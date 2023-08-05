# -*- coding: utf-8 -*-
"""
What it could look like :

msiem 
    --help #Exits after
    --version #Exists after
    --batch

msiem config
    --help
    --list/-l
    --set auth
    --set <section.key>=<value>

msiem esm 
    --help/-h
    --time/-t
    --version/-v
    --tz/--timezones
    --disks/-d
    --callhome
    --ram
    --status
    --backup-status
    --buildstamp
    --recs
    --rule

    #Todo
    --nslookup
    --fields -> display list of possible fields with qryGetSelectFields
    --filters -> display list of possible filters with qryGetFilterFields

    #FullBackUp
    --backup esm_full_backup
    https://github.com/andywalden/esm_full_backup/

msiem ds
    --help/-h
    --add/-a interactive si manque arg
        name=DC01_DNS 
        ip=10.10.1.34 
        rec_ip=172.16.15.10
        type=linux
        Will add a new datasource and also call --info
        Ask for confirmation unless --force

    --del/-d <id or name> if resolves to only one device
        Ask for confirmation unless --force

    --search/-s <pattern>
    --searchgroup/-g
    --info/-i <id or name>
    --times/-t
    (--refresh)
    --recs --> ?
    --ipvalid <>
    --addclient <ds> <> ...

    --checkinactive
    Queries a McAfee ESM for inactive data sources. from https://github.com/andywalden/esmcheckds2

msiem alarms

    --search/-s [default]

    --ack/-a
        Ask for confirmation unless --force

    --del/-d
        Ask for confirmation unless --force

    --unack/-u

    
   
    --time_range LAST_24_HOURS
    --start_time 2019-03-25
    --end_time 2019-03-25
    --status [acked/unacked/all]

    --time 2019-03-25T14:00
    --window 1h

    --filter/-f    
                '[event.]srcip 10.2.2.2'
                '[event.]dstip 10.2.2.1'
                '[event.]msg=http-vulnerability'
                '[event.]count=http-vulnerability'
                '[event.]protocol=http-vulnerability'
                'event.time=http-vulnerability'
                '[event.]subtype=http-vulnerability'

                summary=<>
                severity=90
                ackuser=tristan
                assignee=tristan
                name=Critical
                acktime

                

                #No filtering on DetailedAlarm fields value !
                #Only a couple basic event related fields are available for filtering
                #Filters are ANDed together

    --info/-i <id>
        --> show the conditionnal xml tree and alarm meta data

    --force


msiem events
    --search

    --filter
            -f sourceip=10.2.2.2
            -f destinationip=10.2.2.1
            -f message=http-vulnerability
            -f 'name=Bob le bricoleur'

            -f time=2019-03-25T14:00
            -f window=1h
            -f timerange=LAST_24_HOURS
            -f begins=2019-03-25
            -f ends=2019-03-25

            #and others under event. #See documentation
            #Filters are ANDed together

    --fields
        #Fields to add to the defaults settings

    --order <order>

msiem watchlist
    Inteface to whatchlist operations

msiem service
    Opens a service now mcfee ticket.
    Callable by the Execute function of the ESM.
    https://github.com/andywalden/mfe2snow

msiem syslog
    Generate syslog message on the SIEM

msiem case
    --close https://github.com/andywalden/esm_close_cases
    --open <alarm>
    --msg <message>

msiem elm 
    Export ELM files back to original format
    https://github.com/andywalden/elmex/blob/master/elmex.sh

"""

import argparse
import msiempy
import msiempy.event
import msiempy.alarm

def parse_args():
    parser = argparse.ArgumentParser(description='McAfee SIEM Command Line Interface and Python API',
                usage='Use "msiem <command> --help" for more information.')

    parser.add_argument('--version', help="Show version",action="store_true")
    parser.add_argument('-v', '--verbose', help="Increase output verbosity",action="store_true")

    commands = parser.add_subparsers(dest='command')

    config = commands.add_parser('config')
    config.set_defaults(func=config)
    config.add_argument('--list', help="List configuration fields", action="store_true")
    config.add_argument('--set', help="Will inveractively prompt for configuration settings", action="store_true")

    alarm = commands.add_parser('alarms')
    alarm.set_defaults(func=alarms)

    alarm.add_argument('--action', metavar="action", help="What to do with the alarms: [acknowledge|unacknowledge|delete]")
    alarm.add_argument('--force', help="Will not prompt for confirmation to do the specified action", action="store_true")

    alarm.add_argument('--time_range','-t', metavar='time_range', help='Timerange: '+str(msiempy.FilteredQueryList.POSSIBLE_TIME_RANGE))
    alarm.add_argument('--start_time','--t1', metavar='time', help='Start trigger date')
    alarm.add_argument('--end_time','--t2', metavar='time', help='End trigger date')

    alarm.add_argument('--status', metavar='status', help='Status of the alarm [acknowledged|unacknowledged|all]')

    alarm.add_argument('--filters', '-f', metavar="'<key>=<match>'", nargs='+', type=str, help="""List of filters. Alarm related keys can be :
        - id : The ID of the triggered alarm
        - summary : The summary of the triggered alarm
        - assignee : The assignee for this triggered alarm
        - severity : The severity for this triggered alarm
        - triggeredDate : The date this alarm was triggered
        - acknowledgedDate : The date this triggered alarm was acknowledged
        - acknowledgedUsername : The user that acknowledged this triggered alarm
        - alarmName : The name of the alarm that was triggered
        - events : A string representation of the triggering events
        See : https://mfesiem.github.io/docs/msiempy/alarm.html#msiempy.alarm.Alarm 
        
        Event related keys could be (depending of config) :
        - Rule.msg
        - Alert.SrcPort
        - Alert.DstPort
        - Alert.SrcIP
        - Alert.DstIP
        - Alert.SrcMac
        - Alert.DstMac
        - Alert.LastTime
        - Rule.NormID
        - Alert.DSIDSigID
        - Alert.IPSIDAlertID

        - ruleName
        - srcIp
        - destIp
        - protocol
        - lastTime
        - subtype
        - destPort
        - destMac
        - srcMac
        - srcPort
        - deviceName
        - sigId
        - normId
        - srcUser
        - destUser
        - normMessage
        - normDesc
        - host
        - domain
        - ipsId
        """)

    return (parser.parse_args())

def config(args):

    conf=msiempy.NitroConfig()

    if args.set :
        conf.iset('esm')

    if args.list :
        print(conf)

def alarms(args):

    filters = list()

    #Filers from --filters option
    if args.filters is not None :
        filters+=args.filters

    alarms=msiempy.alarm.AlarmManager(
        time_range=args.time_range,
        start_time=args.start_time,
        end_time=args.end_time,
        status_filter=args.status,
        filters=filters
    ).load_data()

    print(alarms)
        
    if args.action is not None :
        if args.force or ('y' in input('Are you sure you want to '+str(args.action)+' those alarms ? [y/n]')):
            raise NotImplementedError()
            #getattr(alarms, args.action)()

def main():
    args = parse_args()
    print("""
                _                
  _ __ ___  ___(_) ___ _ __ ___  
 | '_ ` _ \/ __| |/ _ | '_ ` _ \ 
 | | | | | \__ | |  __| | | | | |
 |_| |_| |_|___|_|\___|_| |_| |_|
     
 McAfee SIEM Command Line Interface

    """)

    if args.command == 'config' :
        config(args)
    elif args.command == 'alarms' :
        alarms(args)


        """
        #Needs to ignore exception when we call 'msiem command' with no other attributes
        try :
            args.func(args)
        except TypeError as err :
            if "'ArgumentParser' object is not callable" in str(err):
                print("Please refer to documentation.")
            else:
                raise"""

if __name__ == "__main__":
    main()


