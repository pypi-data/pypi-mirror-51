from girder.api import access
from girder.api.describe import describeRoute, Description
from girder.api.rest import boundHandler, filtermodel
from girder.constants import AccessType, TokenScope
from girder.models.collection import Collection as CollectionModel
from .utils import BOUNDS_KEY, computeCollectionConvexHull

COLLECTION_RETURN_FIELDS = ['_id', 'name', BOUNDS_KEY]


@access.public(scope=TokenScope.DATA_READ)
@boundHandler
@describeRoute(
    Description('Query for the items that matches a given geospatial criteria')
    .responseClass('Collection')
    .modelParam('id', model=CollectionModel, level=AccessType.READ)
    .errorResponse('ID was invalid.')
    .errorResponse('Read permission denied on the collection.', 403)
)
def singleCollectionHandler(self, params, id=None):
    collection = CollectionModel().load(id, user=self.getCurrentUser())

    if (BOUNDS_KEY in collection):
        return {k: v for (k, v) in collection.items()
                if k in COLLECTION_RETURN_FIELDS}
    else:
        return {}


@access.public(scope=TokenScope.DATA_READ)
@boundHandler
@describeRoute(
    Description('Get all geometadata of all collections')
    .pagingParams(defaultSort='name')
)
def listCollectionHandler(self, params):
    filteredCollections = []
    for collection in CollectionModel().list(user=self.getCurrentUser()):
        if BOUNDS_KEY in collection:
            filteredCollections.append(
                {k: v for (k, v) in collection.items()
                 if k in COLLECTION_RETURN_FIELDS}
            )

    return filteredCollections


@access.admin
@boundHandler
@describeRoute(
    Description('Force recomputation of all collection convex hulls')
)
def forceRecomputeAllHandler(self, params):
    filteredCollections = []
    for collection in CollectionModel().list(user=self.getCurrentUser()):
        convexHull = computeCollectionConvexHull(
            collection,
            self.getCurrentUser())

        if (convexHull):
            collection[BOUNDS_KEY] = {
                    'type': 'Polygon',
                    'coordinates': [list(convexHull.exterior.coords)]
            }
            collection = CollectionModel().save(collection)

            filteredCollections.append(
                {k: v for (k, v) in collection.items()
                    if k in COLLECTION_RETURN_FIELDS}
            )

    return filteredCollections


@access.admin
@boundHandler
@describeRoute(
    Description('Force delete of all collection convex hulls')
)
def forceDeleteAllHandler(self, params):
    updatedCollections = []
    for collection in CollectionModel().list(user=self.getCurrentUser()):
        if BOUNDS_KEY in collection:
            del collection[BOUNDS_KEY]
            updatedCollections.append(
                {k: v for (k, v) in CollectionModel().save(collection).items()
                    if k in COLLECTION_RETURN_FIELDS}
            )

    return updatedCollections


@access.public(scope=TokenScope.DATA_READ)
@boundHandler
@filtermodel(model=CollectionModel)
@describeRoute(
    Description('Use the mongo query language to do faceted search')
    .jsonParam('query', 'A JSON object containing the mongo query to run',
               paramType='query', requireObject=True)
    # For some reason, paramType needs to be query? (cant be body)
)
def facetedSearchHandler(self, params):
    query = self.getParamJson('query', params)

    docs = CollectionModel().findWithPermissions(
        query=query,
        user=self.getCurrentUser()
    )
    return [doc for doc in docs]
