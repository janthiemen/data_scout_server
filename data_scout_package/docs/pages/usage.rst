Usage
=====
The user interface should be largly self-explanatory, however there are a couple of concepts that are important to know, in order to understand the setup of the system.

- **Projects**: Projects are the primary organizational unit in the tool. Every resource is a part of a project, and you're always working in a project.
- **Data Sources**: A data source defines how data is ingested. There are different types of data sources that can be used, e.g. CSV, Excel or SQL.
- **Flows**: Flows, or recipes as they're sometimes called, are how you define your data preparation pipeline. A flow can either have a data source or a join as input. It then defines transformations that are performed on this input.
- **Wrangler**: The wrangler is where you edit your data flow. It is the place where you define which transformations are applied to your dataset.
- **Join**: Using a join you can combine data sets or flows. A join can act as input to a flow.

In the next steps we'll go through each of the elements and give a quick introduction on how they function together.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   projects
   data_sources
   flows
   wrangler
   settings

