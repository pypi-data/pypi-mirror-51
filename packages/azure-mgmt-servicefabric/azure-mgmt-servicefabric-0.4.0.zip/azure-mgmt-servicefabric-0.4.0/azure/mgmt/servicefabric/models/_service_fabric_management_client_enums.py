# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from enum import Enum


class ProvisioningState(str, Enum):

    updating = "Updating"
    succeeded = "Succeeded"
    failed = "Failed"
    canceled = "Canceled"


class ArmUpgradeFailureAction(str, Enum):

    rollback = "Rollback"  #: Indicates that a rollback of the upgrade will be performed by Service Fabric if the upgrade fails.
    manual = "Manual"  #: Indicates that a manual repair will need to be performed by the administrator if the upgrade fails. Service Fabric will not proceed to the next upgrade domain automatically.


class ServiceCorrelationScheme(str, Enum):

    invalid = "Invalid"  #: An invalid correlation scheme. Cannot be used. The value is zero.
    affinity = "Affinity"  #: Indicates that this service has an affinity relationship with another service. Provided for backwards compatibility, consider preferring the Aligned or NonAlignedAffinity options. The value is 1.
    aligned_affinity = "AlignedAffinity"  #: Aligned affinity ensures that the primaries of the partitions of the affinitized services are collocated on the same nodes. This is the default and is the same as selecting the Affinity scheme. The value is 2.
    non_aligned_affinity = "NonAlignedAffinity"  #: Non-Aligned affinity guarantees that all replicas of each service will be placed on the same nodes. Unlike Aligned Affinity, this does not guarantee that replicas of particular role will be collocated. The value is 3.


class MoveCost(str, Enum):

    zero = "Zero"  #: Zero move cost. This value is zero.
    low = "Low"  #: Specifies the move cost of the service as Low. The value is 1.
    medium = "Medium"  #: Specifies the move cost of the service as Medium. The value is 2.
    high = "High"  #: Specifies the move cost of the service as High. The value is 3.


class PartitionScheme(str, Enum):

    invalid = "Invalid"  #: Indicates the partition kind is invalid. All Service Fabric enumerations have the invalid type. The value is zero.
    singleton = "Singleton"  #: Indicates that the partition is based on string names, and is a SingletonPartitionSchemeDescription object, The value is 1.
    uniform_int64_range = "UniformInt64Range"  #: Indicates that the partition is based on Int64 key ranges, and is a UniformInt64RangePartitionSchemeDescription object. The value is 2.
    named = "Named"  #: Indicates that the partition is based on string names, and is a NamedPartitionSchemeDescription object. The value is 3


class ServiceKind(str, Enum):

    invalid = "Invalid"  #: Indicates the service kind is invalid. All Service Fabric enumerations have the invalid type. The value is zero.
    stateless = "Stateless"  #: Does not use Service Fabric to make its state highly available or reliable. The value is 1.
    stateful = "Stateful"  #: Uses Service Fabric to make its state or part of its state highly available and reliable. The value is 2.


class ServiceLoadMetricWeight(str, Enum):

    zero = "Zero"  #: Disables resource balancing for this metric. This value is zero.
    low = "Low"  #: Specifies the metric weight of the service load as Low. The value is 1.
    medium = "Medium"  #: Specifies the metric weight of the service load as Medium. The value is 2.
    high = "High"  #: Specifies the metric weight of the service load as High. The value is 3.


class ServicePlacementPolicyType(str, Enum):

    invalid = "Invalid"  #: Indicates the type of the placement policy is invalid. All Service Fabric enumerations have the invalid type. The value is zero.
    invalid_domain = "InvalidDomain"  #: Indicates that the ServicePlacementPolicyDescription is of type ServicePlacementInvalidDomainPolicyDescription, which indicates that a particular fault or upgrade domain cannot be used for placement of this service. The value is 1.
    required_domain = "RequiredDomain"  #: Indicates that the ServicePlacementPolicyDescription is of type ServicePlacementRequireDomainDistributionPolicyDescription indicating that the replicas of the service must be placed in a specific domain. The value is 2.
    preferred_primary_domain = "PreferredPrimaryDomain"  #: Indicates that the ServicePlacementPolicyDescription is of type ServicePlacementPreferPrimaryDomainPolicyDescription, which indicates that if possible the Primary replica for the partitions of the service should be located in a particular domain as an optimization. The value is 3.
    required_domain_distribution = "RequiredDomainDistribution"  #: Indicates that the ServicePlacementPolicyDescription is of type ServicePlacementRequireDomainDistributionPolicyDescription, indicating that the system will disallow placement of any two replicas from the same partition in the same domain at any time. The value is 4.
    non_partially_place_service = "NonPartiallyPlaceService"  #: Indicates that the ServicePlacementPolicyDescription is of type ServicePlacementNonPartiallyPlaceServicePolicyDescription, which indicates that if possible all replicas of a particular partition of the service should be placed atomically. The value is 5.


class ArmServicePackageActivationMode(str, Enum):

    shared_process = "SharedProcess"  #: Indicates the application package activation mode will use shared process.
    exclusive_process = "ExclusiveProcess"  #: Indicates the application package activation mode will use exclusive process.
