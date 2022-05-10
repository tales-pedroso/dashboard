# -*- coding: utf-8 -*-
import pandas as pd

# this mapping is repeated in .sql initial statements. ideally, there would be
# only one place in which to draw this relationship from. In case this ever changes,
# both this dict and the INSERT INTO statements in .sql have to changed
# the initial set up should be done from a script too, instead of having .sql
# files
FROM_UG_CODE_TO_UG_ID = {'114601' : '1',
                         '114602' : '2',
                         '114603' : '3',
                         '114604' : '4',
                         '114605' : '5',
                         '114606' : '6',
                         '114607' : '7',
                         '114608' : '8',
                         '114609' : '9',
                         '114610' : '10',
                         '114612' : '11',
                         '114613' : '12',
                         '114614' : '13',
                         '114615' : '14',
                         '114616' : '15',
                         '114617' : '16',
                         '114618' : '17',
                         '114619' : '18',
                         '114620' : '19',
                         '114622' : '20',
                         '114623' : '21',
                         '114624' : '22',
                         '114625' : '23',
                         '114626' : '24',
                         '114627' : '25',
                         '114628' : '26',
                         '114631' : '27',
                         '114639' : '28'}

FROM_UTILITY_CODE_TO_UTILITY_ID = {'07047251000170': '1',
                                   '05965546000109': '2',
                                   '06272793000184': '3',
                                   '04065033000170': '4',
                                   '12272084000100': '5',
                                   '02341467000120': '6',
                                   '15139629000194': '7',
                                   '07522669000192': '8',
                                   '28152650000171': '9',
                                   '27485069000109': '10',
                                   '01377555000110': '11',
                                   '01543032000104': '12',
                                   '19527639000158': '13',
                                   '06981180000116': '14',
                                   '02328280000197': '15',
                                   '15413826000150': '16',
                                   '03467321000199': '17',
                                   '04895728000180': '18',
                                   '08826596000195': '19',
                                   '09095183000140': '20',
                                   '10835932000108': '21',
                                   '06840748000189': '22',
                                   '04368898000106': '23',
                                   '08336783000190': '24',
                                   '61116265000144': '25',
                                   '77882504000107': '26',
                                   '60444437000146': '27',
                                   '33249046000106': '28',
                                   '33050071000158': '29',
                                   '08324196000181': '30',
                                   '05914650000166': '31',
                                   '02341470000144': '32',
                                   '02016439000138': '33',
                                   '08467115000100': '34',
                                   '95289500000100': '35',
                                   '02016440000162': '36',
                                   '88446034000155': '37',
                                   '13255658000196': '38',
                                   '13017462000163': '39',
                                   '61416244000144': '40',
                                   '07282377000120': '41',
                                   '07297359000111': '42',
                                   '33050196000188': '43',
                                   '04172213000151': '44',
                                   '61695227000193': '45',
                                   '02302100000106': '46',
                                   '61015582000174': '47',
                                   '25086034000171': '48'} 

class Filter:
    '''
    base class
    '''
    def __init__(self, series):
        self.series = series
        
    def _process(self):
        pass
    
    def __call__(self):
        self._process()
        return self.series

#==============================================================================
class NewDtype(Filter):
    def __init__(self, series, dtype):
        super().__init__(series)
        self.dtype = dtype
        
    def _process(self):
        # this call is changing month and day when it is a time column
        self.series = self.series.astype(self.dtype) 

class ToFloat(NewDtype):
    def __init__(self, series):
        super().__init__(series, 'float64')
        
class ToDate(NewDtype):
    def __init__(self, series):
        super().__init__(series, 'datetime64')
        
    def _process(self):
        self.series = pd.to_datetime(self.series, dayfirst = True)
    
#==============================================================================
class Replace(Filter):
    def __init__(self, series, from_, to):
        super().__init__(series)
        self.from_ = from_
        self.to    = to
    
    def _process(self):
        self.series = self.series.apply(lambda s: s.replace(self.from_, self.to))
    
class NoDots(Replace):
    def __init__(self, series):
        super().__init__(series, '.', '')
        
class FromCommaToDot(Replace):
    def __init__(self, series):
        super().__init__(series, ',', '.')
        
#==============================================================================
class Remap(Filter):
    def __init__(self, series, mapping):
        super().__init__(series)
        self.mapping = mapping
        
    def _process(self):
        self.series.replace(self.mapping, inplace = True)
        
class RemapUg(Remap):
    def __init__(self, series):
        super().__init__(series, FROM_UG_CODE_TO_UG_ID) # change values

class RemapUtility(Remap):
    def __init__(self, series):
        super().__init__(series, FROM_UTILITY_CODE_TO_UTILITY_ID)
        
#==============================================================================
class Pipe:
    def __init__(self, filters):
        self.filters = filters
    
    def execute(self, series):
        s = series         # s gets transformed along the way
        
        for filter_ in self.filters:
            f = filter_(s) # instanciate
            s = f()        # process series and replace s
            
        return s
    
class DecimalPipe(Pipe):
    def __init__(self):
        filters = (NoDots,          # 9.999,99 -> 9999,99
                   FromCommaToDot,  # 9999,99  -> 9999.00
                   ToFloat)         # object   -> float64
        super().__init__(filters)
        
class DatePipe(Pipe):
    def __init__(self):
        filters = (ToDate,)         # object -> datetime64
        super().__init__(filters)
        
class UgPipe(Pipe):
    def __init__(self):
        filters = (RemapUg,)        # '114601' -> '1'
        super().__init__(filters)

class UtilityPipe(Pipe):
    def __init__(self):
        filters = (RemapUtility,)   # '07047251000170' --> '1'
        super().__init__(filters)
    
#==============================================================================
    
    