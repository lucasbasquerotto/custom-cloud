#!/usr/bin/python

# (c) 2020, Lucas Basquerotto
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=import-error
# pylint: disable=broad-except

# pyright: reportUnusedImport=true
# pyright: reportUnusedVariable=true
# pyright: reportMissingImports=false

from __future__ import absolute_import, division, print_function
__metaclass__ = type  # pylint: disable=invalid-name

from ansible_collections.lrd.cloud.plugins.module_utils.lrd_utils import error_text
from ansible_collections.lrd.ext_cloud.plugins.module_utils.cdn.fastly_cdn import (
    prepare_data as fastly_cdn_prepare_data
)
from ansible_collections.lrd.ext_cloud.plugins.module_utils.cdn.stackpath_cdn import (
    prepare_data as stackpath_cdn_prepare_data
)
from ansible_collections.lrd.ext_cloud.plugins.module_utils.dns.cloudflare_dns import (
    prepare_data as cloudflare_dns_prepare_data
)
from ansible_collections.lrd.ext_cloud.plugins.module_utils.dns.godaddy_dns import (
    prepare_data as godaddy_dns_prepare_data
)
from ansible_collections.lrd.ext_cloud.plugins.module_utils.nameserver.godaddy_nameserver import (
    prepare_data as godaddy_nameserver_prepare_data
)
from ansible_collections.lrd.ext_cloud.plugins.module_utils.s3 import (
    prepare_data as s3_prepare_data
)

from ansible.module_utils._text import to_text
from ansible.module_utils.basic import AnsibleModule

# ===========================================
# Module execution.
#


def main():
  module = AnsibleModule(
      argument_spec=dict(
          identifier=dict(type='str', required=True),
          raw_data=dict(type='raw', required=True),
      )
  )

  identifier = module.params['identifier']
  raw_data = module.params['raw_data']

  info = None
  result = None
  error_msgs = list()

  if not identifier:
    error_msgs += [['msg: identifier not defined']]
  elif identifier == 's3':
    info = s3_prepare_data(raw_data)
  elif identifier == 'godaddy_nameserver':
    info = godaddy_nameserver_prepare_data(raw_data)
  elif identifier == 'godaddy_dns':
    info = godaddy_dns_prepare_data(raw_data)
  elif identifier == 'cloudflare_dns':
    info = cloudflare_dns_prepare_data(raw_data)
  elif identifier == 'fastly_cdn':
    info = fastly_cdn_prepare_data(raw_data)
  elif identifier == 'stackpath_cdn':
    info = stackpath_cdn_prepare_data(raw_data)
  else:
    error_msgs += [['msg: invalid identifier']]

  if info:
    result = info.get('result')
    error_msgs += (info.get('error_msgs') or list())

  if error_msgs:
    context = 'vars module (identifier: ' + str(identifier or '') + ')'
    module.fail_json(msg=to_text(error_text(error_msgs, context)))

  module.exit_json(changed=False, data=result)


if __name__ == '__main__':
  main()
