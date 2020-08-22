from . import math, data, format, count, replace


TRANSFORMATION_MAP = {
    "data-convert": data.Convert,
    "math-add": math.Add,
    "math-min": math.Min,
    "math-multiply": math.Multiply,
    "math-divide": math.Divide,
    "format-uppercase": format.UpperCase,
    "format-lowercase": format.LowerCase,
    "format-trim-whitespace": format.TrimWhitespace,
    "format-trim-quotes": format.TrimQuotes,
    "format-remove-whitespace": format.RemoveWhitespace,
    "format-remove-symbols": format.RemoveSymbols,
    "format-remove-accents": format.RemoveAccents,
    "format-add-prefix": format.AddPrefix,
    "format-add-suffix": format.AddSuffix,
    "format-pad": format.Pad,
    "count-exact": count.CountExact,
    "count-pattern": count.CountRegex,
    "count-delimiters": count.CountDelimiters,
    "replace-text": replace.ReplaceText,
    "replace-regex": replace.ReplaceRegex,
    "replace-delimiters": replace.ReplaceDelimiters,
    "replace-positions": replace.ReplacePositions,
    "replace-mismatched": replace.ReplaceMismatched,
    "replace-missing": replace.ReplaceMissing,
}
