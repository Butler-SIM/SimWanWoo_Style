class FormDataParse:
    """"""

    def parse_nested(self, source, key, nested_keys):
        mutated = source.copy()

        extracted = {}
        for k in nested_keys:
            v = mutated.getlist(f"{key}[{k}]")
            if v:
                extracted[k] = v if len(v) > 1 else v[0]
                mutated.pop(f"{key}[{k}]")

        if len(extracted) > 0:
            self.validate_same_length(extracted.values())
            mutated[key] = extracted

        return mutated

    def validate_same_length(self, values):
        iter_val = iter(values)
        pin = len(next(iter_val))
        if not all(len(v) == pin for v in iter_val):
            raise ValueError("All lists should be same length")
