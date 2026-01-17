# bootseq

**bootseq** is a deterministic bootstrap task sequencing engine.

## Why bootseq?

- Declarative task registration
- Dependency-aware execution
- Parallel execution where safe
- Rollback on failure
- CLI + Python API
- Django-friendly, framework-agnostic

## Usage

```python
from bootseq import register

@register()
def create_roles():
    ...

@register(requires={"myapp.create_roles"})
def create_users():
    ...

```

### Example CLI Usage
```
bootseq plan
bootseq run --tags auth
bootseq run --only auth.create_roles
bootseq run --skip billing.*
bootseq run --dry-run

```


## Installing 

```
pip install git+https://github.com/Ngahu/bootseq.git#egg=bootseq


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