# -*- coding: utf-8 -*-
from config import FROM_UG_CODE_TO_UG_ID, FROM_UTILITY_CODE_TO_UTILITY_ID

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
        self.series = self.series.astype(self.dtype)
        
class ToFloat(NewDtype):
    def __init__(self, series):
        super().__init__(series, 'float64')
        
class ToDate(NewDtype):
    def __init__(self, series):
        super().__init__(series, 'datetime64')
    
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
    def __init__(self, series, col_name, mapping):
        super().__init(series)
        self.col_name = col_name
        self.mapping = mapping
        
    def _process(self):
        self.series.replace({self.col_name: self.mapping}, inplace = True)
        
class RemapUg(Remap):
    def __init__(self, series):
        super().__init__(series, 'ug_code', FROM_UG_CODE_TO_UG_ID) # change values
        self.series.name = 'ug_id'

class RemapUtility(Remap):
    def __init__(self, series):
        super().__init__(series, 'utility_code', FROM_UTILITY_CODE_TO_UTILITY_ID)
        self.series.name = 'utility_id'
        
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
    
    