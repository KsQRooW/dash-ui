class Logic:
    """
    Examples:
        1) ('age', '=', '15')

            expr[0] - 'age'
            expr[1] - '='
            expr[2] - '15'

        2) ('bmi', '!=', '666')
        3) ('region', 'in', ['southwest', 'northeast'])

        ("DF_mask['age'] >= 20",)
        ("DF_mask['age'] >= 20", "DF_mask['bmi'] == 26")
        ("DF_mask['age'] >= 20", "DF_mask['bmi'] == 26", "DF_mask['sex'].isin(['female', 'male'])")
    """
    _swap_symb = {
        'in': ('', '.isin'),  # Pandas method
        'not in': ('~', '.isin')
    }

    mask = "DF_mask"

    def __init__(self):
        self._full_expr = []

    def __call__(self, expr=(None, ), and_or_symbol=None, clear=False):
        self._clear = clear
        self._validate_and_or_symbol(and_or_symbol)
        self._validate_expr(expr)
        return self

    @property
    def full_expr(self):
        res = self._full_expr
        if self._clear:
            self._full_expr = []
        return ''.join(res)

    def _validate_and_or_symbol(self, and_or_symbol):
        if isinstance(and_or_symbol, tuple):
            self._parse_and_or_symbol(and_or_symbol)

    def _parse_and_or_symbol(self, and_or_symbol):
        # Несколько пачек лог выражений, но нет ни одного лог знака
        if len(self._full_expr) > 1:
            if not any(and_or_symbol):
                self._full_expr = self.full_expr[0]
            else:
                iterator_symbols = iter(filter(bool, and_or_symbol))
                k = 0  # чтобы не делать костыли из len(list(filter(bool, and_or_symbol))) и не вызывать filter дважды
                for i in range(len(self._full_expr) - 1):
                    try:
                        self._full_expr[i] += f" {next(iterator_symbols)} "
                        k += 1
                    except StopIteration:
                        break
                self._full_expr = self._full_expr[:k + 1]  # лог выражений всегда на 1 больше, чем лог знаков () & ()

    def _validate_expr(self, expr):
        if all(expr):
            self._parse_expr(expr)

    def _parse_expr(self, expr):
        name = expr[0]
        symbol = expr[1]
        val = expr[2]
        if isinstance(val, list):
            symbol = self._swap_symb[symbol]
            self._full_expr.append(f"{symbol[0]}({self.mask}['{name}']{symbol[1]}({val}))")
        else:
            try:
                self._full_expr.append(f"({self.mask}['{name}'] {symbol} {float(val)})")
            except Exception:
                self._full_expr.append(f"({self.mask}['{name}'] {symbol} '{val}')")
