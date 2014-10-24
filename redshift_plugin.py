import boto
import boto.redshift
import sys

from boundary_aws_plugin.cloudwatch_plugin import CloudwatchPlugin
from boundary_aws_plugin.cloudwatch_metrics import CloudwatchMetrics


class RedshiftCloudwatchMetrics(CloudwatchMetrics):
    def __init__(self, access_key_id, secret_access_key):
        return super(RedshiftCloudwatchMetrics, self).__init__(access_key_id, secret_access_key, 'AWS/Redshift')

    def get_region_list(self):
        return boto.redshift.regions()

    def get_entities_for_region(self, region):
        rs = boto.connect_redshift(self.access_key_id, self.secret_access_key, region=region)
        return rs.describe_clusters()['DescribeClustersResponse']['DescribeClustersResult']['Clusters']

    def get_entity_source_name(self, cluster):
        return cluster['ClusterIdentifier']

    def get_entity_dimensions(self, region, cluster):
        return dict(ClusterIdentifier=cluster['ClusterIdentifier'])

    def get_metric_list(self):
        return (
            ('CPUUtilization', 'Average', 'AWS_REDSHIFT_CPU_UTILIZATION'),
            ('DatabaseConnections', 'Average', 'AWS_REDSHIFT_DATABASE_CONNECTIONS'),
            ('HealthStatus', 'Average', 'AWS_REDSHIFT_HEALTH_STATUS'),
            ('MaintenanceMode', 'Average', 'AWS_REDSHIFT_MAINTENANCE_MODE'),
            ('NetworkReceiveThroughput', 'Average', 'AWS_REDSHIFT_NETWORK_RECEIVE_THROUGHPUT'),
            ('NetworkTransmitThroughput', 'Average', 'AWS_REDSHIFT_NETWORK_TRANSMIT_THROUGHPUT'),
            ('PercentageDiskSpaceUsed', 'Average', 'AWS_REDSHIFT_PERCENTAGE_DISK_SPACE_USED'),
        )


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '-v':
        import logging
        logging.basicConfig(level=logging.INFO)

    plugin = CloudwatchPlugin(RedshiftCloudwatchMetrics, '', 'boundary-plugin-aws-redshift-python-status')
    plugin.main()

