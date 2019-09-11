class DataPrepInputCheck:
    def __init__(self, dataset, logger):
        self.dataset = dataset
        self.logger = logger
    def __set__(self, instance, value):
        if not isinstance(value, dict):
            err_msg = 'Input Loan path shoud be a dict.'
            self.logger.error(err_msg)
            raise ValueError(err_msg)
        else:
            if 'application' not in value:
                err_msg = 'The input dictionary does not have key : application.'
                self.logger.error(err_msg)
                raise ValueError(err_msg)
            elif 'principal' not in value:
                err_msg = 'The input dictionary does not have key :principal.'
                self.logger.error(err_msg)
                raise ValueError(err_msg)                
            else:
                if 'trade_lines' not in value['principal']:
                    err_msg = 'The input dictionary does not have key:tradelines in principal.'
                    self.logger.error(err_msg)
                    raise ValueError(err_msg)
                else:
                    if not isinstance(value['principal']['trade_lines'], list):
                        err_msg = 'Tradelines in principal must be a list of records.'
                        self.logger.error(err_msg)
                        raise ValueError(err_msg)
                if 'inquiries' not in value['principal']:
                    err_msg = 'The input dictionary does not have key:inquiries in principal.'
                    self.logger.error(err_msg)
                    raise ValueError(err_msg) 
                else:
                    if not isinstance(value['principal']['inquiries'], list):
                        err_msg = 'Inquiries in principal must be a list of records.'
                        self.logger.error(err_msg)
                        raise ValueError(err_msg)
                instance.__dict__[self.dataset] = value
                
                


                        