# -*- coding: UTF-8 -*-
#! python3

"""
    Isogeo API v1 - API Routes for Specifications entities

    See: http://help.isogeo.com/api/complete/index.html
"""

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import logging

# 3rd party
from requests.models import Response

# submodules
from isogeo_pysdk.checker import IsogeoChecker
from isogeo_pysdk.decorators import ApiDecorators
from isogeo_pysdk.models import Metadata, Specification
from isogeo_pysdk.utils import IsogeoUtils

# #############################################################################
# ########## Global #############
# ##################################

logger = logging.getLogger(__name__)
checker = IsogeoChecker()
utils = IsogeoUtils()


# #############################################################################
# ########## Classes ###############
# ##################################
class ApiSpecification:
    """Routes as methods of Isogeo API used to manipulate specifications.
    """

    def __init__(self, api_client=None):
        if api_client is not None:
            self.api_client = api_client

        # store API client (Request [Oauthlib] Session) and pass it to the decorators
        self.api_client = api_client
        ApiDecorators.api_client = api_client

        # ensure platform and others params to request
        self.platform, self.api_url, self.app_url, self.csw_url, self.mng_url, self.oc_url, self.ssl = utils.set_base_url(
            self.api_client.platform
        )
        # initialize
        super(ApiSpecification, self).__init__()

    @ApiDecorators._check_bearer_validity
    def listing(
        self,
        workgroup_id: str = None,
        include: list = ["_abilities", "count"],
        caching: bool = 1,
    ) -> list:
        """Get workgroup specifications.

        :param str workgroup_id: identifier of the owner workgroup
        :param list include: additional parts of model to include in response
        :param bool caching: option to cache the response
        """
        # check workgroup UUID
        if not checker.check_is_uuid(workgroup_id):
            raise ValueError("Workgroup ID is not a correct UUID.")
        else:
            pass

        # handling request parameters
        payload = {"_include": include}

        # request URL
        url_specifications = utils.get_request_base_url(
            route="groups/{}/specifications".format(workgroup_id)
        )

        # request
        req_specifications_wg = self.api_client.get(
            url_specifications,
            headers=self.api_client.header,
            params=payload,
            proxies=self.api_client.proxies,
            verify=self.api_client.ssl,
            timeout=self.api_client.timeout,
        )

        # checking response
        req_check = checker.check_api_response(req_specifications_wg)
        if isinstance(req_check, tuple):
            return req_check

        wg_specifications = req_specifications_wg.json()

        # if caching use or store the workgroup specifications
        if caching and not self.api_client._wg_specifications_names:
            self.api_client._wg_specifications_names = {
                i.get("name"): i.get("_id") for i in wg_specifications
            }

        # end of method
        return wg_specifications

    @ApiDecorators._check_bearer_validity
    def specification(self, specification_id: str) -> Specification:
        """Get details about a specific specification.

        :param str specification_id: specification UUID
        """
        # check specification UUID
        if not checker.check_is_uuid(specification_id):
            raise ValueError("specification_id is not a correct UUID.")
        else:
            pass

        # specification route
        url_specification = utils.get_request_base_url(
            route="specifications/{}".format(specification_id)
        )

        # request
        req_specification = self.api_client.get(
            url_specification,
            headers=self.api_client.header,
            proxies=self.api_client.proxies,
            verify=self.api_client.ssl,
            timeout=self.api_client.timeout,
        )

        # checking response
        req_check = checker.check_api_response(req_specification)
        if isinstance(req_check, tuple):
            return req_check

        # end of method
        return Specification(**req_specification.json())

    @ApiDecorators._check_bearer_validity
    def create(
        self,
        workgroup_id: str,
        check_exists: int = 1,
        specification: object = Specification(),
    ) -> Specification:
        """Add a new specification to a workgroup.

        :param str workgroup_id: identifier of the owner workgroup
        :param int check_exists: check if a specification already exists inot the workgroup:

        - 0 = no check
        - 1 = compare name [DEFAULT]

        :param class specification: Specification model object to create
        """
        # check workgroup UUID
        if not checker.check_is_uuid(workgroup_id):
            raise ValueError("Workgroup ID is not a correct UUID.")
        else:
            pass

        # check if specification already exists in workgroup
        if check_exists == 1:
            # retrieve workgroup specifications
            if not self.api_client._wg_specifications_names:
                self.listing(workgroup_id=workgroup_id, include=[])
            # check
            if specification.name in self.api_client._wg_specifications_names:
                logger.debug(
                    "Specification with the same name already exists: {}. Use 'specification_update' instead.".format(
                        specification.name
                    )
                )
                return False
        else:
            pass

        # build request url
        url_specification_create = utils.get_request_base_url(
            route="groups/{}/specifications".format(workgroup_id)
        )

        # request
        req_new_specification = self.api_client.post(
            url_specification_create,
            data=specification.to_dict_creation(),
            headers=self.api_client.header,
            proxies=self.api_client.proxies,
            verify=self.api_client.ssl,
            timeout=self.api_client.timeout,
        )

        # checking response
        req_check = checker.check_api_response(req_new_specification)
        if isinstance(req_check, tuple):
            return req_check

        # load new specification and save it to the cache
        new_specification = Specification(**req_new_specification.json())
        self.api_client._wg_specifications_names[
            new_specification.name
        ] = new_specification._id

        # end of method
        return new_specification

    @ApiDecorators._check_bearer_validity
    def delete(self, workgroup_id: str, specification_id: str) -> dict:
        """Delete a specification from Isogeo database.

        :param str workgroup_id: identifier of the owner workgroup
        :param str specification_id: identifier of the resource to delete
        """
        # check workgroup UUID
        if not checker.check_is_uuid(workgroup_id):
            raise ValueError(
                "Workgroup ID is not a correct UUID: {}".format(workgroup_id)
            )
        else:
            pass

        # check specification UUID
        if not checker.check_is_uuid(specification_id):
            raise ValueError(
                "Specification ID is not a correct UUID: {}".format(specification_id)
            )
        else:
            pass

        # request URL
        url_specification_delete = utils.get_request_base_url(
            route="groups/{}/specifications/{}".format(workgroup_id, specification_id)
        )

        # request
        req_specification_deletion = self.api_client.delete(
            url_specification_delete,
            headers=self.api_client.header,
            proxies=self.api_client.proxies,
            verify=self.api_client.ssl,
            timeout=self.api_client.timeout,
        )

        # checking response
        req_check = checker.check_api_response(req_specification_deletion)
        if isinstance(req_check, tuple):
            return req_check

        return req_specification_deletion

    @ApiDecorators._check_bearer_validity
    def exists(self, specification_id: str) -> bool:
        """Check if the specified specification exists and is available for the authenticated user.

        :param str specification_id: identifier of the specification to verify
        """
        # check specification UUID
        if not checker.check_is_uuid(specification_id):
            raise ValueError(
                "specification_id is not a correct UUID: {}".format(specification_id)
            )
        else:
            pass

        # URL builder
        url_specification_exists = "{}{}".format(
            utils.get_request_base_url("specifications"), specification_id
        )

        # request
        req_specification_exists = self.api_client.get(
            url_specification_exists,
            headers=self.api_client.header,
            proxies=self.api_client.proxies,
            verify=self.api_client.ssl,
            timeout=self.api_client.timeout,
        )

        # checking response
        req_check = checker.check_api_response(req_specification_exists)
        if isinstance(req_check, tuple):
            return req_check

        return req_specification_exists

    @ApiDecorators._check_bearer_validity
    def update(self, specification: Specification, caching: bool = 1) -> Specification:
        """Update a specification owned by a workgroup.

        :param class specification: Specification model object to update
        :param bool caching: option to cache the response
        """
        # check specification UUID
        if not checker.check_is_uuid(specification._id):
            raise ValueError(
                "Specification ID is not a correct UUID: {}".format(specification._id)
            )
        else:
            pass

        # URL
        url_specification_update = utils.get_request_base_url(
            route="groups/{}/specifications/{}".format(
                specification.owner.get("_id"), specification._id
            )
        )

        # request
        req_specification_update = self.api_client.put(
            url=url_specification_update,
            data=specification.to_dict(),
            headers=self.api_client.header,
            proxies=self.api_client.proxies,
            verify=self.api_client.ssl,
            timeout=self.api_client.timeout,
        )

        # checking response
        req_check = checker.check_api_response(req_specification_update)
        if isinstance(req_check, tuple):
            return req_check

        # update specification in cache
        new_specification = Specification(**req_specification_update.json())
        if caching:
            self.api_client._wg_specifications_names[
                new_specification.name
            ] = new_specification._id

        # end of method
        return new_specification

    # -- Routes to manage the related objects ------------------------------------------
    @ApiDecorators._check_bearer_validity
    def associate_metadata(
        self, metadata: Metadata, specification: Specification, conformity: bool = 0
    ) -> Response:
        """Associate a specification (specification + conformity) to a metadata. When a specification is associated to a metadata, it becomes a ResourceConformity object.

        If the specified specification is already associated, the API responses is still a 200.

        :param Metadata metadata: metadata object to update
        :param Specification specification: specification model object to associate
        :param bool conformity: indicates whether the dataset is compliant

        :Example:

        >>> # retrieve objects to be associated
        >>> md = isogeo.metadata.get(
                metadata_id=my_metadata_uuid,
                include=['specifications']
            )
        >>> spec = isogeo.specification.specification(my_specification_uuid)
        >>> # associate them
        >>> isogeo.specification.associate_metadata(
                metadata=md,
                specification=spec,
                conformity=1
            )
        """
        # check metadata UUID
        if not checker.check_is_uuid(metadata._id):
            raise ValueError(
                "Metadata ID is not a correct UUID: {}".format(metadata._id)
            )
        else:
            pass

        # check specification UUID
        if not checker.check_is_uuid(specification._id):
            raise ValueError(
                "Specification ID is not a correct UUID: {}".format(specification._id)
            )
        else:
            pass

        # URL
        url_specification_association = utils.get_request_base_url(
            route="resources/{}/specifications/{}".format(
                metadata._id, specification._id
            )
        )

        # request
        req_specification_association = self.api_client.put(
            url=url_specification_association,
            json={"conformant": conformity, "specification": specification.to_dict()},
            headers=self.api_client.header,
            proxies=self.api_client.proxies,
            verify=self.api_client.ssl,
            timeout=self.api_client.timeout,
        )

        # checking response
        req_check = checker.check_api_response(req_specification_association)
        if isinstance(req_check, tuple):
            return req_check

        # end of method
        return req_specification_association

    @ApiDecorators._check_bearer_validity
    def dissociate_metadata(
        self, metadata: Metadata, specification_id: str
    ) -> Response:
        """Removes the association between a metadata and a specification.

        If the specified specification is not associated, the response is 404.

        :param Metadata metadata: metadata object to update
        :param Specification specification: specification model object to associate
        """
        # check metadata UUID
        if not checker.check_is_uuid(metadata._id):
            raise ValueError(
                "Metadata ID is not a correct UUID: {}".format(metadata._id)
            )
        else:
            pass

        # check specification UUID
        if not checker.check_is_uuid(specification_id):
            raise ValueError(
                "Specification ID is not a correct UUID: {}".format(specification_id)
            )
        else:
            pass

        # URL
        url_specification_dissociation = utils.get_request_base_url(
            route="resources/{}/specifications/{}".format(
                metadata._id, specification_id
            )
        )

        # request
        req_specification_dissociation = self.api_client.delete(
            url=url_specification_dissociation,
            headers=self.api_client.header,
            proxies=self.api_client.proxies,
            verify=self.api_client.ssl,
            timeout=self.api_client.timeout,
        )

        # checking response
        req_check = checker.check_api_response(req_specification_dissociation)
        if isinstance(req_check, tuple):
            return req_check

        # end of method
        return req_specification_dissociation


# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == "__main__":
    """ standalone execution """
    api_specification = ApiSpecification()
    print(api_specification)
