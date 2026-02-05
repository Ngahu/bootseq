

# bootseq

**bootseq** is a deterministic bootstrap sequencing engine for Python projects.

It allows you to define bootstrap tasks across many modules or packages and run them:
- In a predictable order
- With explicit dependencies
- With optional parallel execution
- With rollback support
- Via CLI or Python API



## Install

```bash
pip install git+https://github.com/Ngahu/bootseq.git#egg=bootseq

```


## Usage


Defining Bootstrap Tasks.
Tasks are defined using the `@register` decorator.



Minimal Example (no parameters)
```python
from bootseq import register


@register
def setup_environment():
    print("Setting up environment")

```

This registers a task with:

- Name: `<module>.setup_environment`
- Default order
- No dependencies


Using Parameters

```
@register(
    order=10,
    tags={"core"},
)
def create_config():
    ...
    
```

Dependencies Between Tasks

```
@register
def create_roles():
    ...

@register(requires={"auth.create_roles"})
def create_users():
    ...

```

Dependencies are:

- Explicit

- String-based

- Fully qualified (namespace.task_name)

### Example CLI Usage
```
bootseq plan
bootseq run --tags auth
bootseq run --only auth.create_roles
bootseq run --skip billing.*
bootseq run --dry-run

```




```
+-------------------+
|  App Code / Tasks |
|-------------------|
| @register()       |
| def create_roles():|
|    ...            |
+-------------------+
          |
          v
+-------------------+
|  Registry         |
|-------------------|
| Stores all tasks  |
| Namespaces + IDs  |
| Metadata (tags,   |
| requires, order)  |
+-------------------+
          |
          v
+-------------------+
|  Resolver         |
|-------------------|
| - Compute execution order |
| - Handle dependencies      |
| - Detect circular deps     |
| - Output ordered task list |
+-------------------+
          |
          v
+-------------------+
|  Filters          |
|-------------------|
| - Only / Skip      |
| - Tags filtering   |
| - Returns filtered |
|   task list        |
+-------------------+
          |
          v
+-------------------+
|  Runner           |
|-------------------|
| - Execute tasks    |
| - Respect order    |
| - Parallel safe / sequential batching |
| - Dry-run support  |
| - Rollback on failure |
| - Logging / metrics |
+-------------------+
          |
          v
+-------------------+
|  CLI / Automation |
|-------------------|
| - bootseq run / plan|
| - CLI args → Filters|
| - Invokes Runner   |
+-------------------+
          |
          v
+-------------------+
| Output / Metrics  |
|-------------------|
| Logs, execution time |
| Rollback info       |
| Success/failure     |
+-------------------+
```