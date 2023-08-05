# Copyright 2019, David Wilson
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
# may be used to endorse or promote products derived from this software without
# specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

"""
Stable names for PluginLoader instances across Ansible versions.
"""

from __future__ import absolute_import

__all__ = [
    'action_loader',
    'connection_loader',
    'module_loader',
    'module_utils_loader',
    'shell_loader',
    'strategy_loader',
]

try:
    from ansible.plugins.loader import action_loader
    from ansible.plugins.loader import connection_loader
    from ansible.plugins.loader import module_loader
    from ansible.plugins.loader import module_utils_loader
    from ansible.plugins.loader import shell_loader
    from ansible.plugins.loader import strategy_loader
except ImportError:  # Ansible <2.4
    from ansible.plugins import action_loader
    from ansible.plugins import connection_loader
    from ansible.plugins import module_loader
    from ansible.plugins import module_utils_loader
    from ansible.plugins import shell_loader
    from ansible.plugins import strategy_loader
