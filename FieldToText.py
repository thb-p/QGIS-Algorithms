"""
Field to text :

This script exports data from a specific field
in a map layer to a text file. Options include
field delimiter (separator character), prefix
and suffix characters. Data can be written on
the same line or on separate lines in the file.
"""

from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (QgsProcessing,
                       QgsProcessingException,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterString,
                       QgsProcessingParameterFileDestination,
                       QgsProcessingParameterBoolean)
                       
import csv

class ExportFieldToTextFileAlgorithm(QgsProcessingAlgorithm):
    INPUT_LAYER = 'INPUT_LAYER'
    FIELD_NAME = 'FIELD_NAME'
    DELIMITER = 'DELIMITER'
    PREFIX_CHAR = 'PREFIX_CHAR'
    SUFFIX_CHAR = 'SUFFIX_CHAR'
    SAME_LINE = 'SAME_LINE'
    OUTPUT_FILE = 'OUTPUT_FILE'
    
    def tr(self, string):
        return QCoreApplication.translate('Processing', string)
    
    def createInstance(self):
        return ExportFieldToTextFileAlgorithm()
    
    def name(self):
        return 'exportfieldtotextfile'
    
    def displayName(self):
        return self.tr('Export field to text file')
    
    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterFeatureSource(
            self.INPUT_LAYER,
            self.tr('Input layer'),
        ))
        
        self.addParameter(QgsProcessingParameterString(
                self.FIELD_NAME,
                self.tr('Field name'),
        ))
        
        self.addParameter(QgsProcessingParameterString(
                self.DELIMITER,
                self.tr('Delimiter'),
                defaultValue=', ',
                optional=True
        ))
        
        self.addParameter(QgsProcessingParameterString(
                self.PREFIX_CHAR,
                self.tr('Prefix character'),
                defaultValue='\'',
                optional=True
        ))
        
        self.addParameter(QgsProcessingParameterString(
                self.SUFFIX_CHAR,
                self.tr('Suffix character'),
                defaultValue='\'',
                optional=True
        ))
        
        self.addParameter(QgsProcessingParameterBoolean(
                self.SAME_LINE,
                self.tr('Write elements on the same line'),
                defaultValue=True
        ))        
        
        self.addParameter(QgsProcessingParameterFileDestination(
                self.OUTPUT_FILE,
                self.tr('Output file'),
                'Text Files (*.txt)',
        ))

    def processAlgorithm(self, parameters, context, feedback):
        source = self.parameterAsSource(parameters, self.INPUT_LAYER, context)
        field_name = self.parameterAsString(parameters, self.FIELD_NAME, context)
        delimiter = self.parameterAsString(parameters, self.DELIMITER, context)
        prefix_char = self.parameterAsString(parameters, self.PREFIX_CHAR, context)
        suffix_char = self.parameterAsString(parameters, self.SUFFIX_CHAR, context)
        same_line = self.parameterAsBool(parameters, self.SAME_LINE, context)
        output_file_path = self.parameterAsFileOutput(parameters, self.OUTPUT_FILE, context)
        
        if field_name not in [field.name() for field in source.fields()]:
            raise QgsProcessingException(self.tr("Field name does not exist in the layer."))
        
        separator = delimiter if same_line else delimiter + '\n'
        
        values = []
        
        for feature in source.getFeatures():
            value = str(feature[field_name])
            if prefix_char:
                value = prefix_char + value
            if suffix_char:
                value += suffix_char
            values.append(value)

        with open(output_file_path, 'w') as output_file:
            output_file.write(separator.join(values))

        return {self.OUTPUT_FILE: output_file_path}