# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from future.builtins import *  # NOQA

from .blockette import Blockette
from ..fields import Float, Integer, Loop
from ..utils import Blockette34Lookup, formatRESP


class Blockette055(Blockette):
    """
    Blockette 055: Response List Blockette.

    This blockette alone is not an acceptable response description; always use
    this blockette along with the standard response blockettes ([53], [54],
    [57], or [58]). If this is the only response available, we strongly
    recommend that you derive the appropriate poles and zeros and include
    blockette 53 and blockette 58.
    """

    id = 55
    # Typo is itentional.
    name = "Response list"
    fields = [
        Integer(3, "Stage sequence number", 2),
        Integer(4, "Stage input units", 3, xpath=34),
        Integer(5, "Stage output units", 3, xpath=34),
        Integer(6, "Number of responses listed", 4),
        # REPEAT fields 7 — 11 for the Number of responses listed:
        Loop('Response', "Number of responses listed", [
            Float(7, "Frequency", 12, mask='%+1.5e'),
            Float(8, "Amplitude", 12, mask='%+1.5e'),
            Float(9, "Amplitude error", 12, mask='%+1.5e'),
            Float(10, "Phase angle", 12, mask='%+1.5e'),
            Float(11, "Phase error", 12, mask='%+1.5e')
        ], repeat_title=True)
    ]

    # Changes the name of the blockette because of an error in XSEED 1.0
    def getXML(self, *args, **kwargs):
        xml = Blockette.getXML(self, *args, **kwargs)
        if self.xseed_version == '1.0':
            xml.tag = 'reponse_list'
        return xml

    def getRESP(self, station, channel, abbreviations):
        """
        Returns RESP string.
        """
        string = \
            '#\t\t+                     +---------------------------------+' +\
            '                     +\n' + \
            '#\t\t+                     |   Response List,%6s ch %s   |' + \
            '                     +\n' % (station, channel) + \
            '#\t\t+                     +---------------------------------+' +\
            '                     +\n' + \
            '#\t\t\n' + \
            'B055F03     Stage sequence number:                 %s\n' \
            % self.stage_sequence_number + \
            'B055F04     Response in units lookup:              %s\n' \
            % Blockette34Lookup(abbreviations, self.stage_input_units) + \
            'B055F05     Response out units lookup:             %s\n' \
            % Blockette34Lookup(abbreviations, self.stage_output_units) + \
            'B055F06     Number of responses:                   %s\n' \
            % self.number_of_responses_listed
        if self.number_of_responses_listed:
            string += \
                '#\t\tResponses:\n' + \
                '#\t\t  frequency\t amplitude\t amp error\t    ' + \
                'phase\t phase error\n'
            if self.number_of_responses_listed > 1:
                for _i in range(self.number_of_responses_listed):
                    string += 'B055F07-11  %s\t%s\t%s\t%s\t%s\n' % \
                        (formatRESP(self.frequency[_i], 6),
                         formatRESP(self.amplitude[_i], 6),
                         formatRESP(self.amplitude_error[_i], 6),
                         formatRESP(self.phase_angle[_i], 6),
                         formatRESP(self.phase_error[_i], 6))
            else:
                string += 'B055F07-11  %s\t%s\t%s\t%s\t%s\n' % \
                    (formatRESP(self.frequency, 6),
                     formatRESP(self.amplitude, 6),
                     formatRESP(self.amplitude_error, 6),
                     formatRESP(self.phase_angle, 6),
                     formatRESP(self.phase_error, 6))
        string += '#\t\t\n'
        return string