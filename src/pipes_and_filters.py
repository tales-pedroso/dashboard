# -*- coding: utf-8 -*-
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
    def __init__(self, raw_series):
        super().__init__(raw_series, '.', '')
        
class FromCommaToDot(Replace):
    def __init__(self, raw_series):
        super().__init__(raw_series, ',', '.')
        
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
        
#==============================================================================
    
    