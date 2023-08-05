from datanator_query.util import mongo_util
from datanator_query.query import query_taxon_tree
from pymongo.collation import Collation, CollationStrength
import json

class QueryProtein:

    def __init__(self, username=None, password=None, server=None, authSource='admin',
                 database='datanator', max_entries=float('inf'), verbose=True, collection_str='protein'):

        mongo_manager = mongo_util.MongoUtil(MongoDB=server, username=username,
                                             password=password, authSource=authSource, db=database)
        self.taxon_manager = query_taxon_tree.QueryTaxonTree(MongoDB=server, username=username, password=password,
            authSource=authSource, db=database)
        self.max_entries = max_entries
        self.verbose = verbose
        self.client, self.db, self.collection = mongo_manager.con_db(collection_str)
        self.collation = Collation(locale='en', strength=CollationStrength.SECONDARY)

    def get_meta_by_id(self, _id):
        '''
            Get protein's metadata given uniprot id
            Args:
                _id (:obj: `list` of :obj: `str`): list of uniprot id
            Returns:
                result (:obj: `list` of :obj: `dict`): list of information
        '''
        result = []
        query = {'uniprot_id': {'$in': _id}}
        projection = {'_id': 0, 'ancestor_name': 0, 'ancestor_taxon_id': 0,
                    'kinetics': 0}
        docs = self.collection.find(filter=query, projection=projection, collation=self.collation)
        count = self.collection.count_documents(query, collation=self.collation)

        if count == 0:
            return None

        for doc in docs:
            result.append(doc)
        return result

    def get_meta_by_name_taxon(self, name, taxon_id):
        '''
            Get protein's metadata given protein name
            and its ncbi taxonomy ID
            Args:
                name (:obj: `str`): protein's complete/partial name
                taxon_id (:obj: `int`): protein's ncbi taxonomy id  
            Returns:
                result (:obj: `list` of :obj: `dict`): protein's metadata
        '''
        result = []
        expression = "\"" + name + "\"" 
        query = {'$and': [{'$text': { '$search': expression } },
                         {'ncbi_taxonomy_id': taxon_id}]}
        projection = {'_id': 0, 'ancestor_name': 0, 'ancestor_taxon_id': 0, 'kinetics': 0}
        docs = self.collection.find(filter=query, projection=projection)
        for doc in docs:
            result.append(doc)
        return result


    def get_id_by_name(self, name):
        '''
            Get proteins whose name contains string 'name'
            Args:
                name (:obj: `str`): complete/incomplete protein name
            Returns:
                result (:obj: `list` of :obj: `dict`): list of dictionary containing 
                protein's uniprot_id and name
        '''
        result = []
        expression = "\"" + name + "\"" 
        query = { '$text': { '$search': expression } }
        projection = {'_id': 0, 'uniprot_id': 1, 'protein_name': 1}
        docs = self.collection.find(filter=query, projection=projection)
        # count = self.collection.count_documents(query)
        # if count == 0:
        #     return 'No protein found'
        for doc in docs:
            dic = {'uniprot_id': doc['uniprot_id'], 'protein_name': doc['protein_name']}
            result.append(dic)
        return result

    def get_kinlaw_by_id(self, _id):
        '''
            Get protein kinetic law information by uniprot_id
            Args:
                _id (:obj: `list` of :obj: `str`): list of uniprot IDs
            Returns:
                result (:obj: `list` of `dict`): list of kinlaw information
        '''
        result = []
        query = {'uniprot_id': {'$in': _id}}
        projection = {'_id': 0, 'kinetics': 1, 'taxon': 1, 'uniprot_id': 1}
        docs = self.collection.find(filter=query, projection=projection, collation=self.collation)
        for doc in docs:
            result.append({'uniprot_id': doc.get('uniprot_id'), 'ncbi_taxonomy_id': doc.get('taxon'),
                'similar_functions': doc.get('kinetics')})
        return result

    def get_kinlaw_by_name(self, name):
        '''
        Get protein kinetic law information by protein name
        Args:
            _id: (:obj: `str`): protein's name
        Returns:
            result (:obj: `list` of :obj: `dict`): information
        '''
        entries = self.get_id_by_name(name)
        _ids = []
        for entry in entries:
            _ids.append(entry['uniprot_id'])
        return self.get_kinlaw_by_id(_ids)


    def get_abundance_by_id(self, _id):
        '''
        	Get protein abundance information by uniprot_id
        	Args:
				id (:obj: `list` of :obj: `str`): list of uniprot_id
			Returns:
				result (:obj: `list` of `dict`): list of abundance information
        '''
        result = []
        query = {'uniprot_id': {'$in': _id}}
        
        projection = {'abundances': 1, 'uniprot_id': 1, '_id': 0}
        docs = self.collection.find(filter=query, projection=projection, collation=self.collation)

        for doc in docs:
            result.append(doc)
        return result

    def get_abundance_by_taxon(self, _id):
        '''
            Get protein abundance information in one species
            Args:
                id (:obj: `str`): taxonomy id
            Returns:
                result (:obj: `list` of `dict`): list of abundance information
        '''
        result = []
        query = {'ncbi_taxonomy_id': _id}
        projection = {'ancestor_name': 0, 'ancestor_taxon_id': 0, '_id': 0, 'ncbi_taxonomy_id': 0}
        docs = self.collection.find(filter=query, projection=projection)
        for doc in docs:
            result.append(doc)
        return result


    def get_proximity_abundance_taxon(self, _id, max_distance=3):
        '''
        	Get replacement abundance value by taxonomic distance
        	with the same kegg_orthology number
            Args:
                _id (:obj: `str`): uniprot_id to query for
                max_distance (:obj: `int`): max taxonomic distance from origin protein allowed for
                                            proteins in results
            Returns:
                result (:obj: `list` of :obj: `dict`): list of result proteins and their info 
                    [{'distance': 1, 'documents': [{}, {}, {} ...]}, 
                     {'distance': 2, 'documents': [{}, {}, {} ...]}, ...]
        '''
        if max_distance == 0:
            return 'Please use get_abundance_by_id to check self abundance values'

        result = []
        for i in range(max_distance):
            result.append({'distance': i + 1, 'documents': []})

        query = {'$and': [{'uniprot_id': _id},
                        {'ancestor_taxon_id': {'$exists': True}}] } # needs indexing
        projection = {'ko_number': 1, 'ancestor_taxon_id': 1, 'ancestor_name': 1}
        protein = self.collection.find_one(filter=query, projection=projection,
                                            collation=self.collation)
        if protein == None:
            return 'This protein has no ancestor information to base upon'

        ancestors = protein.get('ancestor_taxon_id')
        names = protein.get('ancestor_name')
        if len(ancestors) < max_distance:
            close_relatives = ancestors
            close_names = names
        else:
            close_relatives = ancestors[-max_distance:]
            close_names = names[-max_distance:]

        ko_number = protein['ko_number']
        query = {'$and':[{'ko_number': ko_number},
                         {'ncbi_taxonomy_id': {'$in': close_relatives}}]} # needs indexing
        projection = {'abundances': 1, 'ncbi_taxonomy_id': 1, 'species_name': 1,
                    'uniprot_id': 1, '_id': 0}
        docs = self.collection.find(filter=query, projection=projection,
                                        collation=self.collation)
        if docs == None:
            return 'No proteins found within constraints'

        for i, doc in enumerate(docs):
            tax_id = doc['ncbi_taxonomy_id']
            distance = max_distance - close_relatives.index(tax_id)
            result[distance-1]['documents'].append(doc)
            result[distance-1]['ancestor_names'] = close_names

        return result


    def get_equivalent_protein(self, _id, max_distance, max_depth=float('inf')):
        '''
            Get replacement abundance value by taxonomic distance
            with the same kegg_orthology number
            Args:
                _id (:obj: `str`): uniprot_id to query for
                max_distance (:obj: `int`): max taxonomic distance from origin protein allowed for
                                            proteins in results
                max_depth (:obj: `int`) max depth allowed from the common node
            Returns:
                result (:obj: `list` of :obj: `dict`): list of result proteins and their info 
                    [{'distance': 1, 'documents': [{}, {}, {} ...]}, 
                     {'distance': 2, 'documents': [{}, {}, {} ...]}, ...]
        '''

        if max_distance <= 0:
            return 'Please use get_abundance_by_id to check self abundance values'
        if max_depth == None:
            max_depth = 1000
        if max_depth <= 0:
            return 'Max_depth has to be greater than 0'

        result = []
        for i in range(max_distance):
            result.append({'distance': i + 1, 'documents': []})

        query = {'uniprot_id': {'$in': _id}}  # needs indexing
        projection = {'ko_number': 1, 'ancestor_taxon_id': 1, 'ancestor_name': 1, 'ncbi_taxonomy_id': 1}
        protein = self.collection.find_one(query, projection=projection, collation=self.collation)
        if protein is None:
            return 'This protein has no ancestor information to base upon'

        ko_number = protein['ko_number']
        ancestor_ids = protein.get('ancestor_taxon_id')
        levels = min(len(ancestor_ids), max_distance)
        checked_ids = [protein['ncbi_taxonomy_id']]

        projection = {'abundances': 1, 'ncbi_taxonomy_id': 1, 'species_name': 1,
                    'uniprot_id': 1, '_id': 0, 'ancestor_taxon_id': 1}
        for level in range(levels):
            cur_id = ancestor_ids[-(level+1)]

            if level == 0:
                common_ancestors = ancestor_ids
            else:                
                common_ancestors = ancestor_ids[:-(level)]
            length = len(common_ancestors)

            query = {'$and': [{'ancestor_taxon_id': {'$all': common_ancestors} },{'ncbi_taxonomy_id': {'$nin': checked_ids} },
                              {'ancestor_taxon_id': {'$nin': checked_ids} }, {'ko_number': ko_number},
                              {'abundances': {'$exists': True} }]}

            equivalents = self.collection.find(filter=query, projection=projection)
            for equivalent in equivalents:
                depth = len(equivalent['ancestor_taxon_id']) - length
                if 0 <= depth < max_depth:
                    equivalent['depth'] = depth + 1
                    tmp = equivalent.pop('ancestor_taxon_id')
                    result[level]['documents'].append(equivalent)
            checked_ids.append(cur_id)
                    
        return result

    def get_uniprot_by_ko(self, ko):
        '''
            Find all proteins with the same kegg orthology id
            Args:
                ko (:obj: `str`): kegg orthology ID
            Return:
                result (:obj: `list` of :obj: `str`): list of uniprot_id
        '''
        ko = ko.upper()
        result = []
        query = {'ko_number': ko}
        projection = {'uniprot_id': 1, '_id': 0}
        docs = self.collection.find(filter=query, projection=projection)
        count = self.collection.count_documents(query)
        
        if count == 0:
            return None

        for doc in docs:
            result.append(doc['uniprot_id'])
        return result

    
    '''
        The methods below are "super" methods that try to predict some 
        commonly used functionalities for modelers
    '''


    def get_abundance_with_same_ko(self, _id):
        '''
            Find abundance information for protein with the same
            KO number
            Args:
                _id (:obj: `str`): uniprot ID
            Returns:
                result (:obj: `list` of :obj: `dict`): information
                [{'ko_number': }, 
                {'uniprot_id': , 'abundances': }, {},...,{}]
        '''

        query = {'uniprot_id': _id}
        projection = {'_id': 0, 'ko_number': 1, 'ncbi_taxonomy_id': 1, 'uniprot_id': 1}
        doc = self.collection.find_one(filter=query, projection=projection, collation=self.collation)
        if doc == None:
            return 'No information available for this protein.'
        ko_number = doc.get('ko_number')
        if ko_number == None:
            return 'No kegg information available for this protein.'
        result = [{'ko_number': ko_number}]
        uniprot_ids = self.get_uniprot_by_ko(ko_number)
        abundance_lists = self.get_abundance_by_id(uniprot_ids)
        meta_lists = self.get_meta_by_id(uniprot_ids)
        for abundance, meta in zip(abundance_lists, meta_lists):
            if abundance.get('abundances') == None:
                continue
            result.append({**meta, **abundance})
        return result