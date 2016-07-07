# Overview

This interface supports integration with BIND using RNDC keys.

# Usage

No explicit handler is required to consume this interface in charms
that consume this interface.

## metadata
To consume this interface in your charm or layer, add the following to `layer.yaml`:

```yaml
includes: ['interface:bind-rndc']
```

and add a requires interface of type `bind-rndc` to your charm or layers
`metadata.yaml`:

```yaml
requires:
  dns-backend:
    interface: bind-rndc
```


## state: {relation\_name}.connected

This state is set when a relation of type bind-rndc is detected, but
the data may not have yet been presented by the providing charm.

## state: {relation\_name}.available

This state is set when the providing application unit  has set all
required data items on the interface.

The interface provides implicit bindings for:

 - `algorithm` - RNDC algorithm to use.
 - `rndckey` - key to use to secure RNDC commands.
 - `private_address` - address of providing application unit.

## handler

```python
@when('dns-backend.available')
def sync_zones(bind_interface):
    sync_all_zones(bind_interface.private_address,
                   bind_interface.algorithm,
                   bind_interface.rndckey)
```

In this case, `sync_all_zones` is a function provided by the consuming
charm.

# Bugs

Please report bugs on [Launchpad](https://bugs.launchpad.net/openstack-charms/+filebug).

For development questions please refer to the OpenStack [Charm Guide](https://github.com/openstack/charm-guide).
