#! /usr/bin/python
#
#   Python script that communicates with the ELMdb web service at CBU
#   WSDL: http://api.bioinfo.no/wsdl/ELMdb.wsdl
#   By Jan Christian Bryne (chrb@ii.uib.no).
#

import SOAPpy, sys
from optparse import OptionParser
from pprint import pprint

def main():
    """Command line interface to the ELM database Web service """

    # parameter parsing configuration
    usage = "usage: %prog [options] (use - as argument to read from stdin) "
    parser = OptionParser(usage=usage)
    parser.add_option("-e", "--elm", action="store", dest="identifier", help="retrive an ELM by identifier")
    parser.add_option("-b", "--elm_by_accession", action="store", dest="accession", help="retrive an ELM by accession")
    parser.add_option("-s", "--elm_search", action="store", dest="text", help="search for ELMs matching given text")
    parser.add_option("-a", "--all_elms", action="store_true", default=False, help="retrive all ELMs")

    parser.add_option("-i", "--instance", action="store", dest="i_accession", help="retrive an ELM instance by accession")
    parser.add_option("-l", "--all_instances", action="store_true", default=False, help="retrive all ELM instances")

    parser.add_option("-f", "--functional_site", action="store", dest="f_accession", help="retrive a functional site by accession")
    parser.add_option("-n", "--functional_site_search", action="store", dest="f_text", help="search for functional sites matching given text")
    parser.add_option("-o", "--all_functional_sites", action="store_true", default=False, help="retrive all functional sites")

    parser.add_option("-v", dest='verbose', action="store_true", default=False, help="print extra details of the returned data")
    parser.add_option("-d", dest='debug', action="store_true", default=False, help="print details of Web service communication")
    (options, args) = parser.parse_args()

   # web service client configuration    
    endpoint = 'http://api.bioinfo.no/services/ELMdb'
    namespace = 'http://elm.eu.org/ELMdb'
    elm_db = SOAPpy.SOAPProxy(endpoint)
    elm_db.namespace = namespace
    elm_db.noroot = 1
    if options.debug:
        elm_db.config.dumpSOAPOut = 1
        elm_db.config.dumpSOAPIn = 1

    try:
        # Retrives an ELM by accession
        if options.accession:
            if options.accession == '-':
                input = sys.stdin.read()[:-1]
            else:
                input = options.accession
            param = SOAPpy.Types.untypedType(input)
            param._name = 'ELMAccession'
            elm = elm_db.getELM(param)
            _print_elm(elm, options.verbose)
            
        # Retrives an ELM by identifier
        elif options.identifier:
            if options.identifier == '-':
                input = sys.stdin.read()[:-1]
            else:
                input = options.identifier
            param = SOAPpy.Types.untypedType(input)
            param._name = 'ELMIdentifier'
            elm = elm_db.getELMByIdentifier(param)
            _print_elm(elm, options.verbose)
    
        # Retrives ELMs based on a search string
        elif options.text:
            if options.text == '-':
                input = sys.stdin.read()[:-1]
            else:
                input = options.text
                param = SOAPpy.Types.untypedType(input)
                param._name = 'QueryText'
                elms = elm_db.getELMsByTextSearch(param)
                _print_elms(elms, options.verbose)
        
        #Retrives all ELMs
        elif options.all_elms:
            elms = elm_db.getAllELMs()
            _print_elms(elms, options.verbose)
            
        # Retrives an ELm instance    
        elif options.i_accession:
            if options.i_accession == '-':
                input = sys.stdin.read()[:-1]
            else:
                input = options.i_accession
            param = SOAPpy.Types.untypedType(input)
            param._name = 'ELMInstanceAccession'
            instance = elm_db.getELMInstance(param)
            _print_instance(instance, options.verbose)
    
    
        # Retrives all ELM instances
        elif options.all_instances:
            instances = elm_db.getAllELMInstances()
            _print_instances(instances, options.verbose)
    
        # Retrives a functional site
        elif options.f_accession:
            if options.f_accession == '-':
                input = sys.stdin.read()[:-1]
            else:
                input = options.f_accession
            param = SOAPpy.Types.untypedType(input)
            param._name = 'FunctionalSiteAccession'
            functional_site = elm_db.getFunctionalSite(param)
            _print_functional_site(functional_site, options.verbose)
    
    
        # Retrives functional sites based on a query string
        elif options.f_text:
            if options.f_text == '-':
                input = sys.stdin.read()[:-1]
            else:
                input = options.f_text
            param = SOAPpy.Types.untypedType(input)
            param._name = 'QueryText'
            functional_sites = elm_db.getFunctionalSitesByTextSearch(param)
            _print_functional_sites(functional_sites, options.verbose)


        # Retrives all functional sites
        elif options.all_functional_sites:
            functional_sites = elm_db.getAllFunctionalSites()
            _print_functional_sites(functional_sites, options.verbose)
            
        else:
            parser.print_help()

    except Exception, e:
        if 'detail' in dir(e):
            if 'ELMAccessionFault' in dir(e.detail):
                print 'No such ELM accession'
            if 'ELMIdentifierFault' in dir(e.detail):
                print 'No such ELM identifier'
            if 'ELMInstanceAccessionFault' in dir(e.detail):
                print 'No such ELM instance accession'
            if 'FunctionalSiteAccessionFault' in dir(e.detail):
                print 'No such functional site accession'
        else:
            print 'Exception:', e


def _print_elm(elm, verbose):
    """Prints the information contained in an ELM to the command line"""
    if not elm:
        sys.exit()
    print 'Identifier: ' + elm.Identifier
    print 'Accession: ' + elm._attrs[(None, 'Accession')]
    print 'Regex: ' + elm.Regex
    print 'Functional site: ' + elm.FunctionalSite
    print 'Description: ' + elm.LongDescription
    print 'Creation date: ' + elm._attrs[(None, 'CreationDate')]
    print 'Change date: ' + elm._attrs[(None, 'ChangeDate')]
    if verbose:
        if 'LiteratureReference' in dir(elm):
            if type(elm.LiteratureReference) == type([]):
                print 'LiteratureReferences:'
                for i in elm.LiteratureReference:
                    print i.Database, 'accession:',i.Accession
            else:
                print 'LiteratureReference:'
                i = elm.LiteratureReference
            print i.Database, 'accession:',i.Accession
        else:
            print 'No LiteratureReferences'
   
        if 'IncludeTaxonomy' in dir(elm):
            if type(elm.IncludeTaxonomy) == type([]):
                for i in elm.IncludeTaxonomy:
                    print 'Include taxonomy:', i.Accession
            else:
                print 'Include taxonomy:',elm.IncludeTaxonomy.Accession
        else:
            print 'No include taxonomy'
        if 'ExcludeTaxonomy' in dir(elm):
            if type(elm.ExcludeTaxonomy) == type([]):
                for i in elm.ExcludeTaxonomy:
                    print 'Exclude taxonomy:', i.Accession
            else:
                print 'Exclude taxonomy:', elm.ExcludeTaxonomy.Accession

        else:
            print 'No exclude taxonomy'
        if 'Instance' in dir(elm):
            if type(elm.Instance) == type([]):
                print 'Instances:'
                instance_list = ""
                for i in elm.Instance:
                    instance_list += i + ' '
                print instance_list
            else:
                print elm.Instance
        else:
            print 'No instances'
        if 'GOterm' in dir(elm):
            if type(elm.GOterm) == type([]):
                print 'Annotated with GO terms:'
                for g in elm.GOterm:
                    if g.ForFiltering == 'true':
                        print g.Accession.Accession, g.Ontology
                    else:
                        print g.Accession.Accession, g.Ontology, '(not for filtering)'
            else:
                if elm.GOterm.ForFiltering == 'true':
                    print 'Annotated with GO term:' + \
                    elm.GOterm.Accession.Accession, elm.GOterm.Ontology
                else:
                    print 'Annotated with GO term:' + \
                    elm.GOterm.Accession.Accession, elm.GOterm.Ontology, '(not for filtering)'             
        else:
            print 'No GO term annotations.'

def _print_elms(elms, verbose):
    """Prints a summery of the information contained in a list of ELMs to the command line"""
    if not type(elms) == type([]):
        _print_elm(elms, verbose)
        sys.exit()
    if verbose:
        for elm in elms:
            _print_elm(elm, verbose)
            print '---------------------------------------------------------------------------'
        sys.exit()
    print 'Accession     Functional site     Identifier               Regex'
    print '----------------------------------------------------------------------------------'
    for elm in elms:
        print elm._attrs[(None, 'Accession')].ljust(14) + elm.FunctionalSite.ljust(20) + \
        elm.Identifier.ljust(25) + elm.Regex

def _print_instance(inst,  verbose):
    """Prints the information contained in an ELM instance to the command line"""
    if not inst:
        sys.exit()
    print 'Accession: ' + inst._attrs[(None, 'Accession')]
    print 'ELM: ' + inst.ELM
    print 'Sequence reference: ' + inst.SequenceReference.Database + ' ' + inst.SequenceReference.Accession
    print 'Start: ' + str(inst.Start)
    print 'End: ' + str(inst.End)
    print 'Creation date: ' + inst._attrs[(None, 'CreationDate')]
    print 'Change date: ' + inst._attrs[(None, 'ChangeDate')]
    if verbose:
        print 'Evidence logic: ' + inst.InstanceLogic
        if 'Evidence' in dir(inst):
            if type(inst.Evidence) == type([]):
                for ev in inst.Evidence:
                    print 'Evidence:'
                    print 'Class: ' + ev.Class
                    print 'Method: ' + ev.Method
                    print 'Logic: ' + ev.Logic
                    print 'Reliability: ' + ev.Reliability
            else:
                print 'Evidence:'
                print 'Class: ' + inst.Evidence.Class
                print 'Method: ' + inst.Evidence.Method
                print 'Logic: ' + inst.Evidence.Logic
                print 'Reliability: ' + inst.Evidence.Reliability
        else:
            print 'Instance have no evidence.'


def _print_instances(insts, verbose):
    """Prints a summery of the information contained in a list of ELM instances to the command line"""
    if not type(insts) == type([]):
        _print_instance(insts)
        sys.exit()
    if verbose:
        for inst in insts:
            _print_instance(inst, verbose)
            print '---------------------------------------------------------------------------'
        sys.exit()
    
    print 'Accession     ELM           Sequence reference  #Evidence'
    print '---------------------------------------------------------'
    for inst in insts:
        str = inst._attrs[(None, 'Accession')].ljust(14) + inst.ELM.ljust(14) + \
        (inst.SequenceReference.Database + ' ' + inst.SequenceReference.Accession).ljust(20) 
        if 'Evidence' in dir(inst):
            if type(inst.Evidence) == type([]):
                str += str(len(inst.Evidence))
            else:
                str += '1'
        else:
            str +='0'
        print str
        

def _print_functional_site(f_site, verbose):
    """Prints the information contained in a functional site to the command line"""
    if not f_site:
        sys.exit()
    print 'Name: ' + f_site.Name
    print 'Accession: ' + f_site._attrs[(None, 'Accession')]
    print 'Title: ' + f_site.DescriptiveTitle
    print 'Description: ' + f_site.ShortDescription
    print 'Creation date: ' + f_site._attrs[(None, 'CreationDate')]
    print 'Change date: ' + f_site._attrs[(None, 'ChangeDate')]
    if verbose:
        if type(f_site.ELM) == type([]):
            print 'ELMs representing this Functional Site:'
            elm_list = ""
            for elm in f_site.ELM:    
                elm_list += elm + ', '
            print elm_list[:-2]
        else:
            print 'ELM representing this Functional Site: ' + f_site.ELM

        if 'Synonym' in dir(f_site):
            if type(f_site.Synonym) == type([]):
                print 'Synonyms:'
                syn_list = ""
                for syn in f_site.Synonym:
                    syn_list += syn + ', '
                print syn_list[:-2]
            else:
                print 'Synonym: ' + f_site.Synonym

        if 'URL' in dir(f_site):
            if type(f_site.URL) == type([]):
                print 'URLs Describing this Functional Site:'
                for url in f_site.URL:
                    print url
            else:
                print 'URL Describing this Functional Site:'
                print f_site.URL

        if 'GOterm' in dir(f_site):
            if type(f_site.GOterm) == type([]):
                print 'Annotated with GO terms:'
                for g in f_site.GOterm:
                    if g.ForFiltering == 'true':
                        print g.Accession.Accession, g.Ontology
                    else:
                        print g.Accession.Accession, g.Ontology, '(not for filtering)'
            else:
                if f_site.GOterm.ForFiltering == 'true':
                    print 'Annotated with GO term:' + \
                    f_site.GOterm.Accession.Accession, elm.GOterm.Ontology
                else:
                    print 'Annotated with GO term:' + \
                    f_site.GOterm.Accession.Accession, elm.GOterm.Ontology, '(not for filtering)'             
        else:
            print 'No GO term annotations.'

def _print_functional_sites(f_sites, verbose):
    """Prints a summery of the information contained in a list of functional sites"""
    if not type(f_sites) == type([]):
        _print_functional_site(f_sites)
        sys.exit()
    if verbose:
        for site in f_sites:
            _print_functional_site(site, verbose)
            print '---------------------------------------------------------------------------'
        sys.exit()
    print 'Accession     Name'
    print '---------------------------------------------------------------'
    for f_site in f_sites:
        print f_site._attrs[(None, 'Accession')].ljust(14) + f_site.Name.ljust(47)

if __name__ == '__main__':
 main ()



