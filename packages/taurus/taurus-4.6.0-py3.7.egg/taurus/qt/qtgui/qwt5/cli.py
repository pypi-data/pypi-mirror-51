#############################################################################
##
# This file is part of Taurus
##
# http://taurus-scada.org
##
# Copyright 2011 CELLS / ALBA Synchrotron, Bellaterra, Spain
##
# Taurus is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
##
# Taurus is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
##
# You should have received a copy of the GNU Lesser General Public License
# along with Taurus.  If not, see <http://www.gnu.org/licenses/>.
##
#############################################################################

import click
from .taurustrend import TaurusTrend


@click.group('qwt5')
def qwt5():
    """Qwt5 related commands"""
    pass


@qwt5.command('plot')
@click.argument('models', nargs=-1)
@click.option('--config', 'config_file', type=click.File('rb'),
              help='configuration file for initialization')
@click.option("-x", "--x-axis-mode", "x_axis_mode",
              type=click.Choice(['t', 'n']),
              default='n',
              show_default=True,
              help=('X axis mode. "t" implies using a Date axis'
                    + '"n" uses the regular axis')
              )
@click.option("--demo", is_flag=True, help="show a demo of the widget")
@click.option('--window-name', 'window_name',
              default='TaurusPlot (qwt5)',
              help='Name of the window')
def plot_cmd(models, config_file, x_axis_mode, demo, window_name):
    """Shows a plot for the given models"""
    from .taurusplot import plot_main
    return plot_main(models=models,
                     config_file=config_file,
                     x_axis_mode=x_axis_mode,
                     demo=demo,
                     window_name=window_name
                     )


@qwt5.command('trend')
@click.argument('models', nargs=-1)
@click.option("-x", "--x-axis-mode", "x_axis_mode",
              type=click.Choice(['t', 'n']),
              default='n',
              show_default=True,
              help=('X axis mode. "t" implies using a Date axis'
                    + '"n" uses the regular axis')
              )
@click.option('-a', '--use-archiving', 'use_archiving',
              is_flag=True,
              default=False,
              help='enable automatic archiving queries')
@click.option('-b', '--buffer', 'max_buffer_size', type=int,
              default=TaurusTrend.DEFAULT_MAX_BUFFER_SIZE,
              show_default=True,
              help='maximum number of values per curve to be plotted')
@click.option('-r', '--forced-read', 'forced_read_period', type=int,
              default=-1,
              metavar="MILLISECONDS",
              help="force re-reading of the attributes every MILLISECONDS ms")
@click.option('--config', 'config_file', type=click.File('rb'),
              help='configuration file for initialization')
@click.option("--demo", is_flag=True, help="show a demo of the widget")
@click.option('--window-name', 'window_name',
              default='TaurusPlot (qwt5)',
              help='Name of the window')
def trend_cmd(models, x_axis_mode, use_archiving, max_buffer_size,
              forced_read_period, config_file, demo, window_name):
    """Shows a trend for the given models"""
    from .taurustrend import trend_main
    return trend_main(models=models,
                      config_file=config_file,
                      x_axis_mode=x_axis_mode,
                      use_archiving=use_archiving,
                      max_buffer_size=max_buffer_size,
                      forced_read_period=forced_read_period,
                      demo=demo,
                      window_name=window_name
                      )


if __name__ == '__main__':
    qwt5()
