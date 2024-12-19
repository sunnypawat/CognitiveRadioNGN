#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# GNU Radio version: 3.10.1.1

from packaging.version import Version as StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from energy_fft_detector import energy_fft_detector  # grc-generated hier_block
from gnuradio import blocks
from gnuradio import gr
from gnuradio.fft import window
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import uhd
import time



from gnuradio import qtgui

class energy_sensing(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Not titled yet")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "energy_sensing")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 1.2e6
        self.threshold = threshold = 350
        self.r_samp = r_samp = 480e3
        self.low_t = low_t = 500
        self.low_pass_tap = low_pass_tap = firdes.low_pass(1.0, samp_rate, 5000,5000, window.WIN_HAMMING, 6.76)
        self.high_t = high_t = 500
        self.ch_space = ch_space = 12.5e3
        self.ch_freq = ch_freq = 446006000
        self.central_freq = central_freq = 446006250
        self.audio_r = audio_r = 48000

        ##################################################
        # Blocks
        ##################################################
        self.uhd_usrp_source_0_0 = uhd.usrp_source(
            ",".join(("", '')),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
        )
        self.uhd_usrp_source_0_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0_0.set_time_unknown_pps(uhd.time_spec(0))

        self.uhd_usrp_source_0_0.set_center_freq(ch_freq, 0)
        self.uhd_usrp_source_0_0.set_antenna("TX/RX", 0)
        self.uhd_usrp_source_0_0.set_normalized_gain(0.8, 0)
        self.qtgui_vector_sink_f_0_4 = qtgui.vector_sink_f(
            2048,
            445000000,
            446000000,
            "x-Axis",
            "y-Axis",
            "0 T",
            1, # Number of inputs
            None # parent
        )
        self.qtgui_vector_sink_f_0_4.set_update_time(0.10)
        self.qtgui_vector_sink_f_0_4.set_y_axis(0, 3)
        self.qtgui_vector_sink_f_0_4.enable_autoscale(False)
        self.qtgui_vector_sink_f_0_4.enable_grid(False)
        self.qtgui_vector_sink_f_0_4.set_x_axis_units("")
        self.qtgui_vector_sink_f_0_4.set_y_axis_units("")
        self.qtgui_vector_sink_f_0_4.set_ref_level(0)

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_vector_sink_f_0_4.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_vector_sink_f_0_4.set_line_label(i, labels[i])
            self.qtgui_vector_sink_f_0_4.set_line_width(i, widths[i])
            self.qtgui_vector_sink_f_0_4.set_line_color(i, colors[i])
            self.qtgui_vector_sink_f_0_4.set_line_alpha(i, alphas[i])

        self._qtgui_vector_sink_f_0_4_win = sip.wrapinstance(self.qtgui_vector_sink_f_0_4.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_vector_sink_f_0_4_win)
        self.qtgui_vector_sink_f_0_3_0 = qtgui.vector_sink_f(
            2048,
            445000000,
            446000000,
            "x-Axis",
            "y-Axis",
            "4 T",
            1, # Number of inputs
            None # parent
        )
        self.qtgui_vector_sink_f_0_3_0.set_update_time(0.10)
        self.qtgui_vector_sink_f_0_3_0.set_y_axis(0, 3)
        self.qtgui_vector_sink_f_0_3_0.enable_autoscale(False)
        self.qtgui_vector_sink_f_0_3_0.enable_grid(False)
        self.qtgui_vector_sink_f_0_3_0.set_x_axis_units("")
        self.qtgui_vector_sink_f_0_3_0.set_y_axis_units("")
        self.qtgui_vector_sink_f_0_3_0.set_ref_level(0)

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_vector_sink_f_0_3_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_vector_sink_f_0_3_0.set_line_label(i, labels[i])
            self.qtgui_vector_sink_f_0_3_0.set_line_width(i, widths[i])
            self.qtgui_vector_sink_f_0_3_0.set_line_color(i, colors[i])
            self.qtgui_vector_sink_f_0_3_0.set_line_alpha(i, alphas[i])

        self._qtgui_vector_sink_f_0_3_0_win = sip.wrapinstance(self.qtgui_vector_sink_f_0_3_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_vector_sink_f_0_3_0_win)
        self.qtgui_vector_sink_f_0_2_1 = qtgui.vector_sink_f(
            2048,
            445000000,
            446000000,
            "x-Axis",
            "y-Axis",
            "3 T",
            1, # Number of inputs
            None # parent
        )
        self.qtgui_vector_sink_f_0_2_1.set_update_time(0.10)
        self.qtgui_vector_sink_f_0_2_1.set_y_axis(0, 3)
        self.qtgui_vector_sink_f_0_2_1.enable_autoscale(False)
        self.qtgui_vector_sink_f_0_2_1.enable_grid(False)
        self.qtgui_vector_sink_f_0_2_1.set_x_axis_units("")
        self.qtgui_vector_sink_f_0_2_1.set_y_axis_units("")
        self.qtgui_vector_sink_f_0_2_1.set_ref_level(0)

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_vector_sink_f_0_2_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_vector_sink_f_0_2_1.set_line_label(i, labels[i])
            self.qtgui_vector_sink_f_0_2_1.set_line_width(i, widths[i])
            self.qtgui_vector_sink_f_0_2_1.set_line_color(i, colors[i])
            self.qtgui_vector_sink_f_0_2_1.set_line_alpha(i, alphas[i])

        self._qtgui_vector_sink_f_0_2_1_win = sip.wrapinstance(self.qtgui_vector_sink_f_0_2_1.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_vector_sink_f_0_2_1_win)
        self.qtgui_vector_sink_f_0_2_0_0 = qtgui.vector_sink_f(
            2048,
            445000000,
            446000000,
            "x-Axis",
            "y-Axis",
            "7 T",
            1, # Number of inputs
            None # parent
        )
        self.qtgui_vector_sink_f_0_2_0_0.set_update_time(0.10)
        self.qtgui_vector_sink_f_0_2_0_0.set_y_axis(0, 3)
        self.qtgui_vector_sink_f_0_2_0_0.enable_autoscale(False)
        self.qtgui_vector_sink_f_0_2_0_0.enable_grid(False)
        self.qtgui_vector_sink_f_0_2_0_0.set_x_axis_units("")
        self.qtgui_vector_sink_f_0_2_0_0.set_y_axis_units("")
        self.qtgui_vector_sink_f_0_2_0_0.set_ref_level(0)

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_vector_sink_f_0_2_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_vector_sink_f_0_2_0_0.set_line_label(i, labels[i])
            self.qtgui_vector_sink_f_0_2_0_0.set_line_width(i, widths[i])
            self.qtgui_vector_sink_f_0_2_0_0.set_line_color(i, colors[i])
            self.qtgui_vector_sink_f_0_2_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_vector_sink_f_0_2_0_0_win = sip.wrapinstance(self.qtgui_vector_sink_f_0_2_0_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_vector_sink_f_0_2_0_0_win)
        self.qtgui_vector_sink_f_0_1_1 = qtgui.vector_sink_f(
            2048,
            445000000,
            446000000,
            "x-Axis",
            "y-Axis",
            "2 T",
            1, # Number of inputs
            None # parent
        )
        self.qtgui_vector_sink_f_0_1_1.set_update_time(0.10)
        self.qtgui_vector_sink_f_0_1_1.set_y_axis(0, 3)
        self.qtgui_vector_sink_f_0_1_1.enable_autoscale(False)
        self.qtgui_vector_sink_f_0_1_1.enable_grid(False)
        self.qtgui_vector_sink_f_0_1_1.set_x_axis_units("")
        self.qtgui_vector_sink_f_0_1_1.set_y_axis_units("")
        self.qtgui_vector_sink_f_0_1_1.set_ref_level(0)

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_vector_sink_f_0_1_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_vector_sink_f_0_1_1.set_line_label(i, labels[i])
            self.qtgui_vector_sink_f_0_1_1.set_line_width(i, widths[i])
            self.qtgui_vector_sink_f_0_1_1.set_line_color(i, colors[i])
            self.qtgui_vector_sink_f_0_1_1.set_line_alpha(i, alphas[i])

        self._qtgui_vector_sink_f_0_1_1_win = sip.wrapinstance(self.qtgui_vector_sink_f_0_1_1.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_vector_sink_f_0_1_1_win)
        self.qtgui_vector_sink_f_0_1_0_0 = qtgui.vector_sink_f(
            2048,
            445000000,
            446000000,
            "x-Axis",
            "y-Axis",
            "6 T",
            1, # Number of inputs
            None # parent
        )
        self.qtgui_vector_sink_f_0_1_0_0.set_update_time(0.10)
        self.qtgui_vector_sink_f_0_1_0_0.set_y_axis(0, 3)
        self.qtgui_vector_sink_f_0_1_0_0.enable_autoscale(False)
        self.qtgui_vector_sink_f_0_1_0_0.enable_grid(False)
        self.qtgui_vector_sink_f_0_1_0_0.set_x_axis_units("")
        self.qtgui_vector_sink_f_0_1_0_0.set_y_axis_units("")
        self.qtgui_vector_sink_f_0_1_0_0.set_ref_level(0)

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_vector_sink_f_0_1_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_vector_sink_f_0_1_0_0.set_line_label(i, labels[i])
            self.qtgui_vector_sink_f_0_1_0_0.set_line_width(i, widths[i])
            self.qtgui_vector_sink_f_0_1_0_0.set_line_color(i, colors[i])
            self.qtgui_vector_sink_f_0_1_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_vector_sink_f_0_1_0_0_win = sip.wrapinstance(self.qtgui_vector_sink_f_0_1_0_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_vector_sink_f_0_1_0_0_win)
        self.qtgui_vector_sink_f_0_0_1 = qtgui.vector_sink_f(
            2048,
            445000000,
            446000000,
            "x-Axis",
            "y-Axis",
            "1 T",
            1, # Number of inputs
            None # parent
        )
        self.qtgui_vector_sink_f_0_0_1.set_update_time(0.10)
        self.qtgui_vector_sink_f_0_0_1.set_y_axis(0, 3)
        self.qtgui_vector_sink_f_0_0_1.enable_autoscale(False)
        self.qtgui_vector_sink_f_0_0_1.enable_grid(False)
        self.qtgui_vector_sink_f_0_0_1.set_x_axis_units("")
        self.qtgui_vector_sink_f_0_0_1.set_y_axis_units("")
        self.qtgui_vector_sink_f_0_0_1.set_ref_level(0)

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_vector_sink_f_0_0_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_vector_sink_f_0_0_1.set_line_label(i, labels[i])
            self.qtgui_vector_sink_f_0_0_1.set_line_width(i, widths[i])
            self.qtgui_vector_sink_f_0_0_1.set_line_color(i, colors[i])
            self.qtgui_vector_sink_f_0_0_1.set_line_alpha(i, alphas[i])

        self._qtgui_vector_sink_f_0_0_1_win = sip.wrapinstance(self.qtgui_vector_sink_f_0_0_1.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_vector_sink_f_0_0_1_win)
        self.qtgui_vector_sink_f_0_0_0_0 = qtgui.vector_sink_f(
            2048,
            445000000,
            446000000,
            "x-Axis",
            "y-Axis",
            "5 T",
            1, # Number of inputs
            None # parent
        )
        self.qtgui_vector_sink_f_0_0_0_0.set_update_time(0.10)
        self.qtgui_vector_sink_f_0_0_0_0.set_y_axis(0, 3)
        self.qtgui_vector_sink_f_0_0_0_0.enable_autoscale(False)
        self.qtgui_vector_sink_f_0_0_0_0.enable_grid(False)
        self.qtgui_vector_sink_f_0_0_0_0.set_x_axis_units("")
        self.qtgui_vector_sink_f_0_0_0_0.set_y_axis_units("")
        self.qtgui_vector_sink_f_0_0_0_0.set_ref_level(0)

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_vector_sink_f_0_0_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_vector_sink_f_0_0_0_0.set_line_label(i, labels[i])
            self.qtgui_vector_sink_f_0_0_0_0.set_line_width(i, widths[i])
            self.qtgui_vector_sink_f_0_0_0_0.set_line_color(i, colors[i])
            self.qtgui_vector_sink_f_0_0_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_vector_sink_f_0_0_0_0_win = sip.wrapinstance(self.qtgui_vector_sink_f_0_0_0_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_vector_sink_f_0_0_0_0_win)
        self.qtgui_sink_x_0 = qtgui.sink_c(
            1024, #fftsize
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "", #name
            True, #plotfreq
            True, #plotwaterfall
            True, #plottime
            True, #plotconst
            None # parent
        )
        self.qtgui_sink_x_0.set_update_time(1.0/10)
        self._qtgui_sink_x_0_win = sip.wrapinstance(self.qtgui_sink_x_0.qwidget(), Qt.QWidget)

        self.qtgui_sink_x_0.enable_rf_freq(False)

        self.top_layout.addWidget(self._qtgui_sink_x_0_win)
        self.qtgui_freq_sink_x_0_0_2_0 = qtgui.freq_sink_c(
            2048, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "Test", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0_0_2_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0_0_2_0.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_0_0_2_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0_0_2_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0_0_2_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0_0_2_0.enable_grid(False)
        self.qtgui_freq_sink_x_0_0_2_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0_0_2_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0_0_2_0.enable_control_panel(False)
        self.qtgui_freq_sink_x_0_0_2_0.set_fft_window_normalized(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0_0_2_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0_0_2_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0_0_2_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0_0_2_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0_0_2_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_0_2_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0_0_2_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_0_0_2_0_win)
        self.energy_fft_detector_0_2 = energy_fft_detector(
            n=5,
            th=high_t,
            tl=low_t,
        )
        self.energy_fft_detector_0_1_0 = energy_fft_detector(
            n=7,
            th=high_t,
            tl=low_t,
        )
        self.energy_fft_detector_0_1 = energy_fft_detector(
            n=3,
            th=high_t,
            tl=low_t,
        )
        self.energy_fft_detector_0_0_1 = energy_fft_detector(
            n=6,
            th=high_t,
            tl=low_t,
        )
        self.energy_fft_detector_0_0_0_0 = energy_fft_detector(
            n=8,
            th=high_t,
            tl=low_t,
        )
        self.energy_fft_detector_0_0_0 = energy_fft_detector(
            n=4,
            th=high_t,
            tl=low_t,
        )
        self.energy_fft_detector_0_0 = energy_fft_detector(
            n=2,
            th=high_t,
            tl=low_t,
        )
        self.energy_fft_detector_0 = energy_fft_detector(
            n=1,
            th=high_t,
            tl=low_t,
        )
        self.blocks_stream_to_vector_1_4 = blocks.stream_to_vector(gr.sizeof_float*1, 2048)
        self.blocks_stream_to_vector_1_3_0 = blocks.stream_to_vector(gr.sizeof_float*1, 2048)
        self.blocks_stream_to_vector_1_2_1 = blocks.stream_to_vector(gr.sizeof_float*1, 2048)
        self.blocks_stream_to_vector_1_2_0_0 = blocks.stream_to_vector(gr.sizeof_float*1, 2048)
        self.blocks_stream_to_vector_1_1_1 = blocks.stream_to_vector(gr.sizeof_float*1, 2048)
        self.blocks_stream_to_vector_1_1_0_0 = blocks.stream_to_vector(gr.sizeof_float*1, 2048)
        self.blocks_stream_to_vector_1_0_1 = blocks.stream_to_vector(gr.sizeof_float*1, 2048)
        self.blocks_stream_to_vector_1_0_0_0 = blocks.stream_to_vector(gr.sizeof_float*1, 2048)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_stream_to_vector_1_0_0_0, 0), (self.qtgui_vector_sink_f_0_0_0_0, 0))
        self.connect((self.blocks_stream_to_vector_1_0_1, 0), (self.qtgui_vector_sink_f_0_0_1, 0))
        self.connect((self.blocks_stream_to_vector_1_1_0_0, 0), (self.qtgui_vector_sink_f_0_1_0_0, 0))
        self.connect((self.blocks_stream_to_vector_1_1_1, 0), (self.qtgui_vector_sink_f_0_1_1, 0))
        self.connect((self.blocks_stream_to_vector_1_2_0_0, 0), (self.qtgui_vector_sink_f_0_2_0_0, 0))
        self.connect((self.blocks_stream_to_vector_1_2_1, 0), (self.qtgui_vector_sink_f_0_2_1, 0))
        self.connect((self.blocks_stream_to_vector_1_3_0, 0), (self.qtgui_vector_sink_f_0_3_0, 0))
        self.connect((self.blocks_stream_to_vector_1_4, 0), (self.qtgui_vector_sink_f_0_4, 0))
        self.connect((self.energy_fft_detector_0, 0), (self.blocks_stream_to_vector_1_4, 0))
        self.connect((self.energy_fft_detector_0, 1), (self.qtgui_freq_sink_x_0_0_2_0, 0))
        self.connect((self.energy_fft_detector_0_0, 0), (self.blocks_stream_to_vector_1_0_1, 0))
        self.connect((self.energy_fft_detector_0_0_0, 0), (self.blocks_stream_to_vector_1_2_1, 0))
        self.connect((self.energy_fft_detector_0_0_0_0, 0), (self.blocks_stream_to_vector_1_2_0_0, 0))
        self.connect((self.energy_fft_detector_0_0_1, 0), (self.blocks_stream_to_vector_1_0_0_0, 0))
        self.connect((self.energy_fft_detector_0_1, 0), (self.blocks_stream_to_vector_1_1_1, 0))
        self.connect((self.energy_fft_detector_0_1_0, 0), (self.blocks_stream_to_vector_1_1_0_0, 0))
        self.connect((self.energy_fft_detector_0_2, 0), (self.blocks_stream_to_vector_1_3_0, 0))
        self.connect((self.uhd_usrp_source_0_0, 0), (self.energy_fft_detector_0, 0))
        self.connect((self.uhd_usrp_source_0_0, 0), (self.energy_fft_detector_0_0, 0))
        self.connect((self.uhd_usrp_source_0_0, 0), (self.energy_fft_detector_0_0_0, 0))
        self.connect((self.uhd_usrp_source_0_0, 0), (self.energy_fft_detector_0_0_0_0, 0))
        self.connect((self.uhd_usrp_source_0_0, 0), (self.energy_fft_detector_0_0_1, 0))
        self.connect((self.uhd_usrp_source_0_0, 0), (self.energy_fft_detector_0_1, 0))
        self.connect((self.uhd_usrp_source_0_0, 0), (self.energy_fft_detector_0_1_0, 0))
        self.connect((self.uhd_usrp_source_0_0, 0), (self.energy_fft_detector_0_2, 0))
        self.connect((self.uhd_usrp_source_0_0, 0), (self.qtgui_sink_x_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "energy_sensing")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_low_pass_tap(firdes.low_pass(1.0, self.samp_rate, 5000, 5000, window.WIN_HAMMING, 6.76))
        self.qtgui_freq_sink_x_0_0_2_0.set_frequency_range(0, self.samp_rate)
        self.qtgui_sink_x_0.set_frequency_range(0, self.samp_rate)
        self.uhd_usrp_source_0_0.set_samp_rate(self.samp_rate)

    def get_threshold(self):
        return self.threshold

    def set_threshold(self, threshold):
        self.threshold = threshold

    def get_r_samp(self):
        return self.r_samp

    def set_r_samp(self, r_samp):
        self.r_samp = r_samp

    def get_low_t(self):
        return self.low_t

    def set_low_t(self, low_t):
        self.low_t = low_t
        self.energy_fft_detector_0.set_tl(self.low_t)
        self.energy_fft_detector_0_0.set_tl(self.low_t)
        self.energy_fft_detector_0_0_0.set_tl(self.low_t)
        self.energy_fft_detector_0_0_0_0.set_tl(self.low_t)
        self.energy_fft_detector_0_0_1.set_tl(self.low_t)
        self.energy_fft_detector_0_1.set_tl(self.low_t)
        self.energy_fft_detector_0_1_0.set_tl(self.low_t)
        self.energy_fft_detector_0_2.set_tl(self.low_t)

    def get_low_pass_tap(self):
        return self.low_pass_tap

    def set_low_pass_tap(self, low_pass_tap):
        self.low_pass_tap = low_pass_tap

    def get_high_t(self):
        return self.high_t

    def set_high_t(self, high_t):
        self.high_t = high_t
        self.energy_fft_detector_0.set_th(self.high_t)
        self.energy_fft_detector_0_0.set_th(self.high_t)
        self.energy_fft_detector_0_0_0.set_th(self.high_t)
        self.energy_fft_detector_0_0_0_0.set_th(self.high_t)
        self.energy_fft_detector_0_0_1.set_th(self.high_t)
        self.energy_fft_detector_0_1.set_th(self.high_t)
        self.energy_fft_detector_0_1_0.set_th(self.high_t)
        self.energy_fft_detector_0_2.set_th(self.high_t)

    def get_ch_space(self):
        return self.ch_space

    def set_ch_space(self, ch_space):
        self.ch_space = ch_space

    def get_ch_freq(self):
        return self.ch_freq

    def set_ch_freq(self, ch_freq):
        self.ch_freq = ch_freq
        self.uhd_usrp_source_0_0.set_center_freq(self.ch_freq, 0)

    def get_central_freq(self):
        return self.central_freq

    def set_central_freq(self, central_freq):
        self.central_freq = central_freq

    def get_audio_r(self):
        return self.audio_r

    def set_audio_r(self, audio_r):
        self.audio_r = audio_r




def main(top_block_cls=energy_sensing, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
