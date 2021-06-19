Wrangler
========
The wrangler is the heart of the data scout tool. This is where you define which transformations are applied to your data. It should feature most, if not all, of the tools you might need to prepare your data for whatever project you're working on. In the future the goal is to include a marketplace where users can share their transformations. 

The wrangler consists of three parts. At the top there is the toolbar, where you add a new transformation to your flow. This flow is shown on the left side of the screen, where you can also change the order of the transformations and edit or delete them. Finally, there is the central data view, where the fruits of your labour are displayed. By clicking the dropdown button next to the column names, you can quickly add a transformation on a specific column.

.. image:: ../assets/wrangler_overview.png
  :alt: An overview of the data wrangler

To add a transformation, simply select a group in the top bar and then select the transformation you need. Alternatively, if you know which transformation you need, you can also press the "Quick access" button or press ``shift`` + ``O`` to open the quick add search bar. This will open a dialog where you can setup the transformation.

.. image:: ../assets/wrangler_transformation.png
  :alt: Select a transformation in the top bar

.. image:: ../assets/wrangler_transformation_dialog.png
  :alt: The transformation dialog

After saving the transformation, it should show up in the overview on the left and the data should be updated to reflect the changes.

.. image:: ../assets/wrangler_export.png
  :alt: The export dialog

When you press the export button on the toolbar, a dialog will open that shows the JSON definition of your pipeline. If you'd like to export it as Python code, simply press the top button in the dialog. This will provide you with an executable Python file.

