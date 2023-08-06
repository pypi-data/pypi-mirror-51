# -*- coding: utf-8 -*-
"""
Created on Sat Aug  3 23:07:15 2019

@author: ydima
"""

import logging
import os
import random
import string
import subprocess
import tempfile
from io import StringIO

import pandas as pd

from .constants import (
    BCPandasException,
    BCPandasValueError,
    _DELIMITER_OPTIONS,
    DIRECTIONS,
    IN,
    NEWLINE,
    OUT,
    QUERY,
    QUERYOUT,
    SQLCHAR,
    TABLE,
    sql_collation,
)

logger = logging.getLogger(__name__)


def bcp(
    sql_item,
    direction,
    flat_file,
    creds,
    sql_type="table",
    schema="dbo",
    format_file_path=None,
    batch_size=None,
):

    combos = {TABLE: [IN, OUT], QUERY: [QUERYOUT]}
    direc = direction.lower()
    # validation
    if direc not in DIRECTIONS:
        raise BCPandasValueError(
            f"Param 'direction' must be one of {DIRECTIONS}, you passed {direc}"
        )
    if direc not in combos[sql_type]:
        raise BCPandasValueError(
            f"Wrong combo of direction and SQL object, you passed {sql_type} and {direc} ."
        )

    # auth
    if creds.with_krb_auth:
        auth = ["-T"]
    else:
        auth = ["-U", creds.username, "-P", creds.password]

    # prepare SQL item string
    if sql_type == QUERY:
        # remove newlines for queries, otherwise messes up BCP
        sql_item_string = "".join(sql_item.splitlines())
    else:
        sql_item_string = f"{schema}.{sql_item}"

    # construct BCP command
    bcp_command = [
        "bcp",
        sql_item_string,
        direc,
        flat_file,
        "-S",
        creds.server,
        "-d",
        creds.database,
        "-q",  # Executes the SET QUOTED_IDENTIFIERS ON statement, needed for Azure SQL DW
    ] + auth

    if batch_size:
        bcp_command += ["-b", str(batch_size)]

    # formats
    if direc == IN:
        bcp_command += ["-f", format_file_path]
    elif direc in (OUT, QUERYOUT):
        bcp_command += [
            "-c",  # marking as character data, not Unicode (maybe make as param?)
            f"-t{_DELIMITER_OPTIONS[0]}",  # marking the delimiter as a comma (maybe also make as param?)
        ]

    # execute
    # TODO better logging and error handling the return stream
    bcp_command_log = [c if c != creds.password else "[REDACTED]" for c in bcp_command]
    logger.info(f"Executing BCP command now... \nBCP command is: {bcp_command_log}")
    result = subprocess.run(
        bcp_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8"
    )
    logger.debug(result.stdout)
    if result.returncode:
        logger.error(result.stdout)
        msg = parse_subprocess_error(result)
        raise BCPandasException(f"Bcp command failed. Details:\n{msg}")


def sqlcmd(creds, command):
    """
    Runs the input command against the database and returns the output if it is a table.
    
    Parameters
    ----------
    creds : bcpandas.SqlCreds
        Creds for the database
    command : str
        SQL command to be executed against the server
    
    Returns
    --------------------
    Pandas.DataFrame or None
        Returns a table if the command has an output. Returns None if the output does not return anything.
    """
    if creds.with_krb_auth:
        auth = ["-E"]
    else:
        auth = ["-U", creds.username, "-P", creds.password]
    if '"' in command:
        raise BCPandasValueError(
            'Cannot have double quotes charachter (") in the command, '
            "raises problems when combining the sqlcmd utility with Python"
        )
    command = f"set nocount on; {command} "
    sqlcmd_command = (
        ["sqlcmd", "-S", creds.server, "-d", creds.database, "-b"]
        + auth
        # set quoted identifiers ON, needed for Azure SQL Data Warehouse
        # see https://docs.microsoft.com/en-us/azure/sql-data-warehouse/sql-data-warehouse-get-started-connect-sqlcmd
        + ["-I"]
        + ["-s,", "-W", "-Q", command]
    )

    # execute
    # TODO better logging and error handling the return stream
    sqlcmd_command_log = [c if c != creds.password else "[REDACTED]" for c in sqlcmd_command]
    logger.info(f"Executing SqlCmd command now... \nSqlCmd command is: {sqlcmd_command_log}")
    result = subprocess.run(
        sqlcmd_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8"
    )
    logger.debug(result.stdout)
    if result.returncode:
        logger.error(result.stdout)
        msg = parse_subprocess_error(result)
        raise BCPandasException(f"SqlCmd command failed. Details:\n{msg}")

    output = StringIO(result.stdout)
    first_line_output = output.readline().strip()
    if first_line_output == "":
        header = None
    else:
        header = "infer"
    output.seek(0)
    try:
        result = pd.read_csv(filepath_or_buffer=output, skiprows=[1], header=header)
    except pd.errors.EmptyDataError:
        result = None
    return result


def get_temp_file():
    """
    Returns full path to a temporary file without creating it.
    """
    tmp_dir = tempfile.gettempdir()
    file_path = os.path.join(
        tmp_dir, "".join(random.choices(string.ascii_letters + string.digits, k=21))
    )
    return file_path


def _escape(input_string):
    """
    Adopted from https://github.com/titan550/bcpy/blob/master/bcpy/format_file_builder.py#L25
    """
    return (
        input_string.replace('"', '\\"')
        .replace("'", "\\'")
        .replace("\r", "\\r")
        .replace("\n", "\\n")
    )


def build_format_file(df, delimiter):
    """
    Creates the non-xml SQL format file. Puts 4 spaces between each section.
    See https://docs.microsoft.com/en-us/sql/relational-databases/import-export/non-xml-format-files-sql-server
    for the specification of the file.

    # TODO add params/options to control:
    #   - the char type (not just SQLCHAR),
    #   - the ability to skip destination columns

    Parameters
    ----------
    df : pandas DataFrame
    delimiter : a valid delimiter character

    Returns
    -------
    A string containing the format file
    """
    _space = " " * 4
    format_file_str = f"9.0\n{len(df.columns)}\n"  # Version and Number of columns
    for col_num, col_name in enumerate(df.columns, start=1):
        # last col gets a newline sep
        _delim = delimiter if col_num != len(df.columns) else NEWLINE
        _line = _space.join(
            [
                str(col_num),  # Host file field order
                SQLCHAR,  # Host file data type
                str(0),  # Prefix length
                str(0),  # Host file data length
                f'"{_escape(_delim)}"',  # Terminator (see note below)
                str(col_num),  # Server column order
                col_name,  # Server column name, optional as long as not blank
                sql_collation,  # Column collation
                "\n",
            ]
        )
        format_file_str += _line
    # FYI very important to surround the Terminator with quotes, otherwise BCP fails with:
    # "Unexpected EOF encountered in BCP data-file". Hugely frustrating bug.
    return format_file_str


def _get_sql_create_statement(df, table_name, schema="dbo"):
    """
    Creates a SQL drop and re-create statement corresponding to the columns list of the object.
    
    Parameters
    -------------
    df : pandas DataFrame
    table_name : str
        name of the new table
    
    Returns
    -------------
    SQL code to create the table
    """
    sql_cols = ",".join(map(lambda x: f"[{x}] nvarchar(max)", df.columns))
    sql_command = (
        f"if object_id('[dbo].[{table_name}]', 'U') "
        f"is not null drop table [dbo].[{table_name}];"
        f"create table [dbo].[{table_name}] ({sql_cols});"
    )
    return sql_command


def parse_subprocess_error(result):
    msg = {}
    for item in ["args", "returncode", "stdout", "stderr"]:
        _i = getattr(result, item)
        msg[item] = _i.decode() if isinstance(_i, bytes) else _i
    return msg
