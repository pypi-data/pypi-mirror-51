"""
Inline Source
-------------

Example configuration (YAML):

.. code-block:: yaml

   sources:
     - type: inline
       config:
         instances:
           - instance_id: my_service
             service_clusters:
               - P2
             parameters:
               upstream_address:
                 - address: service.domain.com
                   region: us-east-1
             plan_id: 7d57270a-0348-58d3-829d-447a98fe98d5
"""
from sovereign.sources.lib import Source


class Inline(Source):
    def __init__(self, *args, **kwargs):
        super(Inline, self).__init__(*args, **kwargs)
        for arg in args:
            if not isinstance(arg, dict):
                continue
            self.instances = arg['instances']

    def get(self):
        """ Returns the data passed via configuration """
        return self.instances
