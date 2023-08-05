# OmicsTools

Suite of tools to enable processing and functional analysis of -omics data. 

 * Normalization and filtering counts data
 * Namespace conversion
 * GO enrichment

See `example/demo.ipynb`.

# Installation

`pip install OmicsTools`


# Development

Generate distribution archive
`python3 setup.py sdist bdist_wheel`

Upload new distributions
`twine upload --skip-existing dist/*`