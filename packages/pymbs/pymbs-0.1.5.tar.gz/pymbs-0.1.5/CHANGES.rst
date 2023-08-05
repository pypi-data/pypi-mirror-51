==========
Change Log
==========

0.1.5
-----

Changes:
~~~~~~~~

- Fixed an issue with missing package config/data


0.1.0
-----

Changes:
~~~~~~~~

- Significant update to Configuration management. Created new Config object
  to hold configuration settings. Provide ability to set settings via YAML
  file and/or environment variables.

- Added some basic logging, especially in the Config object.

- Significant updates to documentation.


0.0.2
-----

Changes:
~~~~~~~~

- Significant update to intital architecture, but still in alpa stage.

- Run cash flows for *Assumed Collateral* replines only.

- Implement payment functionality for the following payment rule types:
    * Calculate (*Basic* functioanlity for calulating buckets of cash)
    * Pay Accrue, for Z bond accrual
    * Pay Pro Rata
    * Pay Sequential

- Generates cash flows for any waterfall that makes use of the above rules.

- Introduces the Tranche object, to enable flexibilty when making payments
  to tranches from the waterfall. This appears to be a much better approach
  than trying to use Pandas DataFrames for this task. Once the cash flows
  have been generated for the tranche, they are converted to a DataFrame
  for display and use in a Jupyter Notebook.

- Calculate Weighted Average Lives (WALs) for all tranches in the model that
  are paid using one of the pay rules described above.


0.0.1
-----

Changes:
~~~~~~~~

- Initial version.
