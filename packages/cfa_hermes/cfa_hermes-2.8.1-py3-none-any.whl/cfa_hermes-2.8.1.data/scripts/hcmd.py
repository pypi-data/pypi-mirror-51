#!python
# coding: utf-8
#-----------------------------------------------------------------
# hermes: hcmd.py
#
# hermes command line tool
#
# Copyright (C) 2016-2019, Christophe Fauchard
#-----------------------------------------------------------------

import hermes
import zeus
import argparse
import os
import configparser
import paramiko
import logging

#
# command line parsing
#
args_parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
args_parser.add_argument("--version", action='version', version='%(prog)s ' + hermes.__version__)
args_parser.add_argument("file", help="""
hermes config file structured as bellow:

Mandatory keys:

[hermes]

name = name of the transfer
user = chris

cryptedpassword = crypted password using zcrypt utility
or
private_key = private key path

host = hostname or ip

protocol = sftp or ftp

deleteflag = yes or no
activation = yes or no
command = put or get

localdir = tmp/upload/sample_sftp_get2
remotedir = tmp


Optional keys:

port = custom connection port

excluderegex = exclude files containing the mmotif
               (not match all)
includeregex = regex if file contain the motif,
               it is transfered (not match all)
transferedext = extension to add to correct transfered files

statuslogdir = path of the status directory
backupdir = path of the backup directory

logfile = path of the rotated log file

localdir1 = tmp/upload/sample_sftp_get2_1
localdir2 = tmp/upload/sample_sftp_get2_2
localdir3 = tmp/upload/sample_sftp_get2_3
localdir4 = tmp/upload/sample_sftp_get2_4

""")
args_parser.add_argument("--zkey", help="zeus secret key")
args = args_parser.parse_args()

try:

    #
    # display version and config informations
    #
    print("hermes version: " + hermes.__version__)
    print("zeus version: " + zeus.__version__)

    print("hermes config file: " + args.file)

    #
    # ZPK variable set with option in command line
    #
    if args.zkey is not None:
        os.environ["ZPK"] = args.zkey
        print("zeus key:", args.zkey)

    #
    # create an hermes connection object
    #
    connection = hermes.connection.Connection(args.file)
    connection.log.set_level(logging.INFO)
    connection.connect()
    connection.start()
    connection.close()

#
# exceptions handling
#
except hermes.exception.AuthenticationException as error:
    print("ERROR: authentication exception", error.username, error.private_key)
    connection.last_connection(-1, "authentication exception")
except zeus.exception.InvalidConfigurationFileException as error:
    print("ERROR: invalid configuration file", error.filename)
except zeus.exception.PrivateKeyException:
    print("ERROR: ZPK variable for zeus key not set")
except hermes.exception.ActivationException:
    print("WARNING: not activated")
except hermes.exception.ProtocolUnsupportedException as error:
    print("ERROR: protocol unsupported", error.protocol)
except configparser.NoOptionError as error:
    print("ERROR missing key", error.option, "in section", error.section)
except hermes.exception.CommandUnsupportedException as error:
    print("ERROR unsupported command", error.command)
except hermes.exception.ChdirException as error:
    print("ERROR change directory", error.dir)
except zeus.exception.FileNotFoundException as error:
    print("ERROR file not found", error.filename)
except paramiko.ssh_exception.SSHException as error:
    print("ERROR sftp connexion", error.username)
