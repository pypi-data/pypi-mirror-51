# pyUntis

Initial working prototype for a Python parser for Untis substitution tables

## Todo

- Cleanup and modularize code
- Parse information field
- export JSON

## Usage

    import pyuntis
    
    untis = pyuntis.PyUntis(data)
    print(untis.parse())