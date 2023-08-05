from collections import defaultdict
from decimal import Decimal
import io
import json
import logging
from pathlib import Path
import pkg_resources
from typing import Sequence

import attr

from ai.backend.common.logging import BraceStyleAdapter
from ai.backend.common.types import BinarySize, ResourceAllocations, ResourceSlot
from ..exception import InitializationError
from ..resources import Mount

log = BraceStyleAdapter(logging.getLogger('ai.backend.agent.resources'))

known_slot_types = {}


@attr.s(auto_attribs=True, slots=True)
class KernelResourceSpec:
    '''
    This struct-like object stores the kernel resource allocation information
    with serialization and deserialization.

    It allows seamless reconstruction of allocations even when the agent restarts
    while kernel containers are running.
    '''

    '''The container ID to refer inside containers.'''
    container_id: str

    '''Stores the original user-requested resource slots.'''
    slots: ResourceSlot

    '''
    Represents the resource allocations for each slot (device) type and devices.
    '''
    allocations: ResourceAllocations

    '''The mounted vfolder list.'''
    mounts: Sequence[str] = attr.Factory(list)

    '''The size of scratch disk. (not implemented yet)'''
    scratch_disk_size: int = None

    '''The idle timeout in seconds.'''
    idle_timeout: int = None

    def write_to_file(self, file: io.TextIOBase):
        '''
        Write the current resource specification into a file-like object.
        '''
        file.write(f'CID={self.container_id}\n')
        file.write(f'SCRATCH_SIZE={BinarySize(self.scratch_disk_size):m}\n')
        mounts_str = ','.join(map(str, self.mounts))
        file.write(f'MOUNTS={mounts_str}\n')
        slots_str = json.dumps({
            k: str(v) for k, v in self.slots.items()
        })
        file.write(f'SLOTS={slots_str}\n')
        file.write(f'IDLE_TIMEOUT={self.idle_timeout}\n')
        for device_type, slots in self.allocations.items():
            for slot_type, per_device_alloc in slots.items():
                pieces = []
                for dev_id, alloc in per_device_alloc.items():
                    if known_slot_types[slot_type] == 'bytes':
                        pieces.append(f'{dev_id}:{BinarySize(alloc):s}')
                    else:
                        pieces.append(f'{dev_id}:{alloc}')
                alloc_str = ','.join(pieces)
                file.write(f'{slot_type.upper()}_SHARES={alloc_str}\n')

    def write_to_text(self) -> str:
        mounts_str = ','.join(map(str, self.mounts))
        slots_str = json.dumps({
            k: str(v) for k, v in self.slots.items()
        })

        resource_str = f'CID={self.container_id}\n'
        resource_str += f'SCRATCH_SIZE={BinarySize(self.scratch_disk_size):m}\n'
        resource_str += f'MOUNTS={mounts_str}\n'
        resource_str += f'SLOTS={slots_str}\n'
        resource_str += f'IDLE_TIMEOUT={self.idle_timeout}\n'

        for device_type, slots in self.allocations.items():
            for slot_type, per_device_alloc in slots.items():
                pieces = []
                for dev_id, alloc in per_device_alloc.items():
                    if known_slot_types[slot_type] == 'bytes':
                        pieces.append(f'{dev_id}:{BinarySize(alloc):s}')
                    else:
                        pieces.append(f'{dev_id}:{alloc}')
                alloc_str = ','.join(pieces)
                resource_str += f'{slot_type.upper()}_SHARES={alloc_str}\n'

        return resource_str

    @classmethod
    def read_from_text(cls, text: str):
        kvpairs = {}
        for line in text.split('\n'):
            if '=' not in line:
                continue
            key, val = line.strip().split('=', maxsplit=1)
            kvpairs[key] = val
        allocations = defaultdict(dict)
        for key, val in kvpairs.items():
            if key.endswith('_SHARES'):
                slot_type = key[:-7].lower()
                device_type = slot_type.split('.')[0]
                per_device_alloc = {}
                for entry in val.split(','):
                    dev_id, _, alloc = entry.partition(':')
                    if not dev_id or not alloc:
                        continue
                    try:
                        if known_slot_types[slot_type] == 'bytes':
                            value = BinarySize.from_str(alloc)
                        else:
                            value = Decimal(alloc)
                    except KeyError as e:
                        log.warning('A previously launched container has '
                                    'unknown slot type: {}. Ignoring it.',
                                    e.args[0])
                        continue
                    per_device_alloc[dev_id] = value
                allocations[device_type][slot_type] = per_device_alloc
        mounts = [Mount.from_str(m) for m in kvpairs['MOUNTS'].split(',') if m]
        return cls(
            container_id=kvpairs.get('CID'),
            scratch_disk_size=BinarySize.from_str(kvpairs['SCRATCH_SIZE']),
            allocations=dict(allocations),
            slots=ResourceSlot(json.loads(kvpairs['SLOTS'])),
            mounts=mounts,
            idle_timeout=int(kvpairs.get('IDLE_TIMEOUT', '600')),
        )

    @classmethod
    def read_from_file(cls, file: io.TextIOBase):
        '''
        Read resource specification values from a file-like object.
        '''
        kvpairs = {}
        for line in file:
            key, val = line.strip().split('=', maxsplit=1)
            kvpairs[key] = val
        allocations = defaultdict(dict)
        for key, val in kvpairs.items():
            if key.endswith('_SHARES'):
                slot_type = key[:-7].lower()
                device_type = slot_type.split('.')[0]
                per_device_alloc = {}
                for entry in val.split(','):
                    dev_id, _, alloc = entry.partition(':')
                    if not dev_id or not alloc:
                        continue
                    try:
                        if known_slot_types[slot_type] == 'bytes':
                            value = BinarySize.from_str(alloc)
                        else:
                            value = Decimal(alloc)
                    except KeyError as e:
                        log.warning('A previously launched container has '
                                    'unknown slot type: {}. Ignoring it.',
                                    e.args[0])
                        continue
                    per_device_alloc[dev_id] = value
                allocations[device_type][slot_type] = per_device_alloc
        mounts = [Mount.from_str(m) for m in kvpairs['MOUNTS'].split(',') if m]
        return cls(
            container_id=kvpairs.get('CID'),
            scratch_disk_size=BinarySize.from_str(kvpairs['SCRATCH_SIZE']),
            allocations=dict(allocations),
            slots=ResourceSlot(json.loads(kvpairs['SLOTS'])),
            mounts=mounts,
            idle_timeout=int(kvpairs.get('IDLE_TIMEOUT', '600')),
        )

    def to_json(self) -> str:
        o = attr.asdict(self)
        for slot_type, alloc in o['slots'].items():
            if known_slot_types[slot_type] == 'bytes':
                o['slots'] = f'{BinarySize(alloc):s}'
            else:
                o['slots'] = str(alloc)
        for dev_type, dev_alloc in o['allocations'].items():
            for slot_type, per_device_alloc in dev_alloc.items():
                for dev_id, alloc in per_device_alloc.items():
                    if known_slot_types[slot_type] == 'bytes':
                        alloc = f'{BinarySize(alloc):s}'
                    else:
                        alloc = str(alloc)
                    o['allocations'][dev_type][slot_type][dev_id] = alloc
        o['mounts'] = list(map(str, self.mounts))
        return json.dumps(o)


async def detect_resources(etcd, reserved_slots):
    '''
    Detect available computing resource of the system.
    It also loads the accelerator plugins.

    limit_cpus, limit_gpus are deprecated.
    '''

    slots = {}

    from .intrinsic import CPUPlugin, MemoryPlugin

    compute_device_types = {}
    compute_device_types[CPUPlugin.key] = CPUPlugin
    compute_device_types[MemoryPlugin.key] = MemoryPlugin

    entry_prefix = 'backendai_accelerator_v12'
    for entrypoint in pkg_resources.iter_entry_points(entry_prefix):
        log.info('loading accelerator plugin: {}', entrypoint.module_name)
        plugin = entrypoint.load()
        plugin_config = await etcd.get_prefix_dict(f'config/plugins/{plugin.PREFIX}')
        # TODO: scaling group-specific configs
        accel_klass = await plugin.init(plugin_config)
        if accel_klass is None:
            # plugin init failed. skip!
            continue
        if not all(skey.startswith(f'{accel_klass.key}.') for skey, _ in accel_klass.slot_types):
            raise InitializationError(
                "Slot types defined by an accelerator plugin must be prefixed "
                "by the plugin's key.")
        if accel_klass.key in compute_device_types:
            raise InitializationError(
                f"A plugin defining the same key '{accel_klass.key}' already exists. "
                "You may need to uninstall it first.")
        compute_device_types[accel_klass.key] = accel_klass

    for key, klass in compute_device_types.items():
        known_slot_types.update(klass.slot_types)
        resource_slots = await klass.available_slots()
        for skey, sval in resource_slots.items():
            slots[skey] = max(0, sval - reserved_slots.get(skey, 0))
            if slots[skey] <= 0 and skey in ('cpu', 'mem'):
                raise InitializationError(
                    f"The resource slot '{skey}' is not sufficient (zero or below zero). "
                    "Try to adjust the reserved resources or use a larger machine.")

    log.info('Resource slots: {!r}', slots)
    log.info('Slot types: {!r}', known_slot_types)
    return compute_device_types, slots


async def get_resource_spec_from_container(container):
    for mount in container['HostConfig']['Mounts']:
        if mount['Target'] == '/home/config':
            with open(Path(mount['Source']) / 'resource.txt', 'r') as f:
                return KernelResourceSpec.read_from_file(f)
            break
    else:
        return None
