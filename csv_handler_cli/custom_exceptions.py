
class FilePathNotProvided(Exception):
    """Exception in case a path to the csv file is not provided, or it is not a valid one"""

class FilterAndAggregateSimultaneousUsage(Exception):
    """Exception in case both main flags are used"""

class NotAcceptableOperatorOrName(Exception):
    """Exception raises when not acceptable operator was used
    or name for specified flag not in a lis of eligible ones"""

class OrderByAggregateFlagsConflict(Exception):
    """Exception raises when order by flag is used with aggregate flag"""