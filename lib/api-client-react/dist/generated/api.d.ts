import type { QueryKey, UseMutationOptions, UseMutationResult, UseQueryOptions, UseQueryResult } from '@tanstack/react-query';
import type { Analytics, Approval, ApprovalAction, ChatInput, ChatResponse, Dashboard, DecisionTwin, DiscoverVendorsParams, HealthStatus, ListPurchaseRequestsParams, ListVendorsParams, Notification, PurchaseOrder, PurchaseOrderDetail, PurchaseOrderInput, PurchaseRequest, PurchaseRequestDetail, PurchaseRequestInput, PurchaseRequestList, TrackingItem, Vendor, VendorComparison, VendorDetail, VendorDiscoveryRequest, VendorDiscoveryResponse, VendorInput, VendorList, VendorPerformance } from './api.schemas';
import { customFetch } from '../custom-fetch';
import type { ErrorType, BodyType } from '../custom-fetch';
type AwaitedInput<T> = PromiseLike<T> | T;
type Awaited<O> = O extends AwaitedInput<infer T> ? T : never;
type SecondParameter<T extends (...args: never) => unknown> = Parameters<T>[1];
export declare const getHealthCheckUrl: () => string;
/**
 * @summary Health check
 */
export declare const healthCheck: (options?: Parameters<typeof customFetch>[1]) => Promise<HealthStatus>;
export declare const getHealthCheckQueryKey: () => readonly ["/api/healthz"];
export declare const getHealthCheckQueryOptions: <TData = Awaited<ReturnType<typeof healthCheck>>, TError = ErrorType<unknown>>(options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof healthCheck>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}) => UseQueryOptions<Awaited<ReturnType<typeof healthCheck>>, TError, TData> & {
    queryKey: QueryKey;
};
export type HealthCheckQueryResult = NonNullable<Awaited<ReturnType<typeof healthCheck>>>;
export type HealthCheckQueryError = ErrorType<unknown>;
/**
 * @summary Health check
 */
export declare function useHealthCheck<TData = Awaited<ReturnType<typeof healthCheck>>, TError = ErrorType<unknown>>(options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof healthCheck>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}): UseQueryResult<TData, TError> & {
    queryKey: QueryKey;
};
export declare const getLoginUrl: () => string;
/**
 * @summary User login
 */
export declare const login: (loginBody: LoginBody, options?: Parameters<typeof customFetch>[1]) => Promise<LoginResponse>;
export declare const getLoginMutationOptions: <TError = ErrorType<unknown>, TContext = unknown>(options?: {
    mutation?: UseMutationOptions<Awaited<ReturnType<typeof login>>, TError, {
        data: BodyType<LoginBody>;
    }, TContext>;
    request?: SecondParameter<typeof customFetch>;
}) => UseMutationOptions<Awaited<ReturnType<typeof login>>, TError, {
    data: BodyType<LoginBody>;
}, TContext>;
export type LoginMutationResult = NonNullable<Awaited<ReturnType<typeof login>>>;
export type LoginMutationBody = BodyType<LoginBody>;
export type LoginMutationError = ErrorType<unknown>;
/**
* @summary User login
*/
export declare const useLogin: <TError = ErrorType<unknown>, TContext = unknown>(options?: {
    mutation?: UseMutationOptions<Awaited<ReturnType<typeof login>>, TError, {
        data: BodyType<LoginBody>;
    }, TContext>;
    request?: SecondParameter<typeof customFetch>;
}) => UseMutationResult<Awaited<ReturnType<typeof login>>, TError, {
    data: BodyType<LoginBody>;
}, TContext>;
export declare const getGetDashboardUrl: () => string;
/**
 * @summary Get procurement dashboard
 */
export declare const getDashboard: (options?: Parameters<typeof customFetch>[1]) => Promise<Dashboard>;
export declare const getGetDashboardQueryKey: () => readonly ["/api/v1/dashboard"];
export declare const getGetDashboardQueryOptions: <TData = Awaited<ReturnType<typeof getDashboard>>, TError = ErrorType<unknown>>(options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof getDashboard>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}) => UseQueryOptions<Awaited<ReturnType<typeof getDashboard>>, TError, TData> & {
    queryKey: QueryKey;
};
export type GetDashboardQueryResult = NonNullable<Awaited<ReturnType<typeof getDashboard>>>;
export type GetDashboardQueryError = ErrorType<unknown>;
/**
 * @summary Get procurement dashboard
 */
export declare function useGetDashboard<TData = Awaited<ReturnType<typeof getDashboard>>, TError = ErrorType<unknown>>(options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof getDashboard>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}): UseQueryResult<TData, TError> & {
    queryKey: QueryKey;
};
export declare const getListPurchaseRequestsUrl: (params?: ListPurchaseRequestsParams) => string;
/**
 * @summary List purchase requests
 */
export declare const listPurchaseRequests: (params?: ListPurchaseRequestsParams, options?: Parameters<typeof customFetch>[1]) => Promise<PurchaseRequestList>;
export declare const getListPurchaseRequestsQueryKey: (params?: ListPurchaseRequestsParams) => readonly ["/api/v1/purchase-requests", ...ListPurchaseRequestsParams[]];
export declare const getListPurchaseRequestsQueryOptions: <TData = Awaited<ReturnType<typeof listPurchaseRequests>>, TError = ErrorType<unknown>>(params?: ListPurchaseRequestsParams, options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof listPurchaseRequests>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}) => UseQueryOptions<Awaited<ReturnType<typeof listPurchaseRequests>>, TError, TData> & {
    queryKey: QueryKey;
};
export type ListPurchaseRequestsQueryResult = NonNullable<Awaited<ReturnType<typeof listPurchaseRequests>>>;
export type ListPurchaseRequestsQueryError = ErrorType<unknown>;
/**
 * @summary List purchase requests
 */
export declare function useListPurchaseRequests<TData = Awaited<ReturnType<typeof listPurchaseRequests>>, TError = ErrorType<unknown>>(params?: ListPurchaseRequestsParams, options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof listPurchaseRequests>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}): UseQueryResult<TData, TError> & {
    queryKey: QueryKey;
};
export declare const getCreatePurchaseRequestUrl: () => string;
/**
 * @summary Create a purchase request
 */
export declare const createPurchaseRequest: (purchaseRequestInput: PurchaseRequestInput, options?: Parameters<typeof customFetch>[1]) => Promise<PurchaseRequest>;
export declare const getCreatePurchaseRequestMutationOptions: <TError = ErrorType<unknown>, TContext = unknown>(options?: {
    mutation?: UseMutationOptions<Awaited<ReturnType<typeof createPurchaseRequest>>, TError, {
        data: BodyType<PurchaseRequestInput>;
    }, TContext>;
    request?: SecondParameter<typeof customFetch>;
}) => UseMutationOptions<Awaited<ReturnType<typeof createPurchaseRequest>>, TError, {
    data: BodyType<PurchaseRequestInput>;
}, TContext>;
export type CreatePurchaseRequestMutationResult = NonNullable<Awaited<ReturnType<typeof createPurchaseRequest>>>;
export type CreatePurchaseRequestMutationBody = BodyType<PurchaseRequestInput>;
export type CreatePurchaseRequestMutationError = ErrorType<unknown>;
/**
* @summary Create a purchase request
*/
export declare const useCreatePurchaseRequest: <TError = ErrorType<unknown>, TContext = unknown>(options?: {
    mutation?: UseMutationOptions<Awaited<ReturnType<typeof createPurchaseRequest>>, TError, {
        data: BodyType<PurchaseRequestInput>;
    }, TContext>;
    request?: SecondParameter<typeof customFetch>;
}) => UseMutationResult<Awaited<ReturnType<typeof createPurchaseRequest>>, TError, {
    data: BodyType<PurchaseRequestInput>;
}, TContext>;
export declare const getGetPurchaseRequestUrl: (id: number) => string;
/**
 * @summary Get purchase request details
 */
export declare const getPurchaseRequest: (id: number, options?: Parameters<typeof customFetch>[1]) => Promise<PurchaseRequestDetail>;
export declare const getGetPurchaseRequestQueryKey: (id: number) => readonly [`/api/v1/purchase-requests/${number}`];
export declare const getGetPurchaseRequestQueryOptions: <TData = Awaited<ReturnType<typeof getPurchaseRequest>>, TError = ErrorType<unknown>>(id: number, options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof getPurchaseRequest>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}) => UseQueryOptions<Awaited<ReturnType<typeof getPurchaseRequest>>, TError, TData> & {
    queryKey: QueryKey;
};
export type GetPurchaseRequestQueryResult = NonNullable<Awaited<ReturnType<typeof getPurchaseRequest>>>;
export type GetPurchaseRequestQueryError = ErrorType<unknown>;
/**
 * @summary Get purchase request details
 */
export declare function useGetPurchaseRequest<TData = Awaited<ReturnType<typeof getPurchaseRequest>>, TError = ErrorType<unknown>>(id: number, options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof getPurchaseRequest>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}): UseQueryResult<TData, TError> & {
    queryKey: QueryKey;
};
export declare const getListApprovalsUrl: () => string;
/**
 * @summary List approval tasks
 */
export declare const listApprovals: (options?: Parameters<typeof customFetch>[1]) => Promise<Approval[]>;
export declare const getListApprovalsQueryKey: () => readonly ["/api/v1/approvals"];
export declare const getListApprovalsQueryOptions: <TData = Awaited<ReturnType<typeof listApprovals>>, TError = ErrorType<unknown>>(options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof listApprovals>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}) => UseQueryOptions<Awaited<ReturnType<typeof listApprovals>>, TError, TData> & {
    queryKey: QueryKey;
};
export type ListApprovalsQueryResult = NonNullable<Awaited<ReturnType<typeof listApprovals>>>;
export type ListApprovalsQueryError = ErrorType<unknown>;
/**
 * @summary List approval tasks
 */
export declare function useListApprovals<TData = Awaited<ReturnType<typeof listApprovals>>, TError = ErrorType<unknown>>(options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof listApprovals>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}): UseQueryResult<TData, TError> & {
    queryKey: QueryKey;
};
export declare const getApproveRequestUrl: (id: number) => string;
/**
 * @summary Approve a request
 */
export declare const approveRequest: (id: number, approvalAction?: ApprovalAction, options?: Parameters<typeof customFetch>[1]) => Promise<Approval>;
export declare const getApproveRequestMutationOptions: <TError = ErrorType<unknown>, TContext = unknown>(options?: {
    mutation?: UseMutationOptions<Awaited<ReturnType<typeof approveRequest>>, TError, {
        id: number;
        data?: BodyType<ApprovalAction>;
    }, TContext>;
    request?: SecondParameter<typeof customFetch>;
}) => UseMutationOptions<Awaited<ReturnType<typeof approveRequest>>, TError, {
    id: number;
    data?: BodyType<ApprovalAction>;
}, TContext>;
export type ApproveRequestMutationResult = NonNullable<Awaited<ReturnType<typeof approveRequest>>>;
export type ApproveRequestMutationBody = BodyType<ApprovalAction> | undefined;
export type ApproveRequestMutationError = ErrorType<unknown>;
/**
* @summary Approve a request
*/
export declare const useApproveRequest: <TError = ErrorType<unknown>, TContext = unknown>(options?: {
    mutation?: UseMutationOptions<Awaited<ReturnType<typeof approveRequest>>, TError, {
        id: number;
        data?: BodyType<ApprovalAction>;
    }, TContext>;
    request?: SecondParameter<typeof customFetch>;
}) => UseMutationResult<Awaited<ReturnType<typeof approveRequest>>, TError, {
    id: number;
    data?: BodyType<ApprovalAction>;
}, TContext>;
export declare const getRejectRequestUrl: (id: number) => string;
/**
 * @summary Reject a request
 */
export declare const rejectRequest: (id: number, approvalAction?: ApprovalAction, options?: Parameters<typeof customFetch>[1]) => Promise<Approval>;
export declare const getRejectRequestMutationOptions: <TError = ErrorType<unknown>, TContext = unknown>(options?: {
    mutation?: UseMutationOptions<Awaited<ReturnType<typeof rejectRequest>>, TError, {
        id: number;
        data?: BodyType<ApprovalAction>;
    }, TContext>;
    request?: SecondParameter<typeof customFetch>;
}) => UseMutationOptions<Awaited<ReturnType<typeof rejectRequest>>, TError, {
    id: number;
    data?: BodyType<ApprovalAction>;
}, TContext>;
export type RejectRequestMutationResult = NonNullable<Awaited<ReturnType<typeof rejectRequest>>>;
export type RejectRequestMutationBody = BodyType<ApprovalAction> | undefined;
export type RejectRequestMutationError = ErrorType<unknown>;
/**
* @summary Reject a request
*/
export declare const useRejectRequest: <TError = ErrorType<unknown>, TContext = unknown>(options?: {
    mutation?: UseMutationOptions<Awaited<ReturnType<typeof rejectRequest>>, TError, {
        id: number;
        data?: BodyType<ApprovalAction>;
    }, TContext>;
    request?: SecondParameter<typeof customFetch>;
}) => UseMutationResult<Awaited<ReturnType<typeof rejectRequest>>, TError, {
    id: number;
    data?: BodyType<ApprovalAction>;
}, TContext>;
export declare const getListVendorsUrl: (params?: ListVendorsParams) => string;
/**
 * @summary List vendors
 */
export declare const listVendors: (params?: ListVendorsParams, options?: Parameters<typeof customFetch>[1]) => Promise<VendorList>;
export declare const getListVendorsQueryKey: (params?: ListVendorsParams) => readonly ["/api/v1/vendors", ...ListVendorsParams[]];
export declare const getListVendorsQueryOptions: <TData = Awaited<ReturnType<typeof listVendors>>, TError = ErrorType<unknown>>(params?: ListVendorsParams, options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof listVendors>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}) => UseQueryOptions<Awaited<ReturnType<typeof listVendors>>, TError, TData> & {
    queryKey: QueryKey;
};
export type ListVendorsQueryResult = NonNullable<Awaited<ReturnType<typeof listVendors>>>;
export type ListVendorsQueryError = ErrorType<unknown>;
/**
 * @summary List vendors
 */
export declare function useListVendors<TData = Awaited<ReturnType<typeof listVendors>>, TError = ErrorType<unknown>>(params?: ListVendorsParams, options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof listVendors>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}): UseQueryResult<TData, TError> & {
    queryKey: QueryKey;
};
export declare const getCreateVendorUrl: () => string;
/**
 * @summary Create a vendor
 */
export declare const createVendor: (vendorInput: VendorInput, options?: Parameters<typeof customFetch>[1]) => Promise<Vendor>;
export declare const getCreateVendorMutationOptions: <TError = ErrorType<unknown>, TContext = unknown>(options?: {
    mutation?: UseMutationOptions<Awaited<ReturnType<typeof createVendor>>, TError, {
        data: BodyType<VendorInput>;
    }, TContext>;
    request?: SecondParameter<typeof customFetch>;
}) => UseMutationOptions<Awaited<ReturnType<typeof createVendor>>, TError, {
    data: BodyType<VendorInput>;
}, TContext>;
export type CreateVendorMutationResult = NonNullable<Awaited<ReturnType<typeof createVendor>>>;
export type CreateVendorMutationBody = BodyType<VendorInput>;
export type CreateVendorMutationError = ErrorType<unknown>;
/**
* @summary Create a vendor
*/
export declare const useCreateVendor: <TError = ErrorType<unknown>, TContext = unknown>(options?: {
    mutation?: UseMutationOptions<Awaited<ReturnType<typeof createVendor>>, TError, {
        data: BodyType<VendorInput>;
    }, TContext>;
    request?: SecondParameter<typeof customFetch>;
}) => UseMutationResult<Awaited<ReturnType<typeof createVendor>>, TError, {
    data: BodyType<VendorInput>;
}, TContext>;
export declare const getGetVendorUrl: (id: number) => string;
/**
 * @summary Get vendor details
 */
export declare const getVendor: (id: number, options?: Parameters<typeof customFetch>[1]) => Promise<VendorDetail>;
export declare const getGetVendorQueryKey: (id: number) => readonly [`/api/v1/vendors/${number}`];
export declare const getGetVendorQueryOptions: <TData = Awaited<ReturnType<typeof getVendor>>, TError = ErrorType<unknown>>(id: number, options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof getVendor>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}) => UseQueryOptions<Awaited<ReturnType<typeof getVendor>>, TError, TData> & {
    queryKey: QueryKey;
};
export type GetVendorQueryResult = NonNullable<Awaited<ReturnType<typeof getVendor>>>;
export type GetVendorQueryError = ErrorType<unknown>;
/**
 * @summary Get vendor details
 */
export declare function useGetVendor<TData = Awaited<ReturnType<typeof getVendor>>, TError = ErrorType<unknown>>(id: number, options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof getVendor>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}): UseQueryResult<TData, TError> & {
    queryKey: QueryKey;
};
export declare const getContactVendorUrl: (id: number) => string;
/**
 * @summary Contact a vendor
 */
export declare const contactVendor: (id: number, contactVendorBody: ContactVendorBody, options?: Parameters<typeof customFetch>[1]) => Promise<ContactVendor200>;
export declare const getContactVendorMutationOptions: <TError = ErrorType<unknown>, TContext = unknown>(options?: {
    mutation?: UseMutationOptions<Awaited<ReturnType<typeof contactVendor>>, TError, {
        id: number;
        data: BodyType<ContactVendorBody>;
    }, TContext>;
    request?: SecondParameter<typeof customFetch>;
}) => UseMutationOptions<Awaited<ReturnType<typeof contactVendor>>, TError, {
    id: number;
    data: BodyType<ContactVendorBody>;
}, TContext>;
export type ContactVendorMutationResult = NonNullable<Awaited<ReturnType<typeof contactVendor>>>;
export type ContactVendorMutationBody = BodyType<ContactVendorBody>;
export type ContactVendorMutationError = ErrorType<unknown>;
/**
* @summary Contact a vendor
*/
export declare const useContactVendor: <TError = ErrorType<unknown>, TContext = unknown>(options?: {
    mutation?: UseMutationOptions<Awaited<ReturnType<typeof contactVendor>>, TError, {
        id: number;
        data: BodyType<ContactVendorBody>;
    }, TContext>;
    request?: SecondParameter<typeof customFetch>;
}) => UseMutationResult<Awaited<ReturnType<typeof contactVendor>>, TError, {
    id: number;
    data: BodyType<ContactVendorBody>;
}, TContext>;
export declare const getDiscoverVendorsUrl: (params?: DiscoverVendorsParams) => string;
/**
 * @summary Discover vendors for a product
 */
export declare const discoverVendors: (params?: DiscoverVendorsParams, options?: Parameters<typeof customFetch>[1]) => Promise<Vendor[]>;
export declare const getDiscoverVendorsQueryKey: (params?: DiscoverVendorsParams) => readonly ["/api/v1/vendors/discover", ...DiscoverVendorsParams[]];
export declare const getDiscoverVendorsQueryOptions: <TData = Awaited<ReturnType<typeof discoverVendors>>, TError = ErrorType<unknown>>(params?: DiscoverVendorsParams, options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof discoverVendors>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}) => UseQueryOptions<Awaited<ReturnType<typeof discoverVendors>>, TError, TData> & {
    queryKey: QueryKey;
};
export type DiscoverVendorsQueryResult = NonNullable<Awaited<ReturnType<typeof discoverVendors>>>;
export type DiscoverVendorsQueryError = ErrorType<unknown>;
/**
 * @summary Discover vendors for a product
 */
export declare function useDiscoverVendors<TData = Awaited<ReturnType<typeof discoverVendors>>, TError = ErrorType<unknown>>(params?: DiscoverVendorsParams, options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof discoverVendors>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}): UseQueryResult<TData, TError> & {
    queryKey: QueryKey;
};
export declare const getDiscoverBulkVendorsUrl: () => string;
/**
 * @summary Discover qualified vendors for a bulk order
 */
export declare const discoverBulkVendors: (vendorDiscoveryRequest: VendorDiscoveryRequest, options?: Parameters<typeof customFetch>[1]) => Promise<VendorDiscoveryResponse>;
export declare const getDiscoverBulkVendorsMutationOptions: <TError = ErrorType<void>, TContext = unknown>(options?: {
    mutation?: UseMutationOptions<Awaited<ReturnType<typeof discoverBulkVendors>>, TError, {
        data: BodyType<VendorDiscoveryRequest>;
    }, TContext>;
    request?: SecondParameter<typeof customFetch>;
}) => UseMutationOptions<Awaited<ReturnType<typeof discoverBulkVendors>>, TError, {
    data: BodyType<VendorDiscoveryRequest>;
}, TContext>;
export type DiscoverBulkVendorsMutationResult = NonNullable<Awaited<ReturnType<typeof discoverBulkVendors>>>;
export type DiscoverBulkVendorsMutationBody = BodyType<VendorDiscoveryRequest>;
export type DiscoverBulkVendorsMutationError = ErrorType<void>;
/**
* @summary Discover qualified vendors for a bulk order
*/
export declare const useDiscoverBulkVendors: <TError = ErrorType<void>, TContext = unknown>(options?: {
    mutation?: UseMutationOptions<Awaited<ReturnType<typeof discoverBulkVendors>>, TError, {
        data: BodyType<VendorDiscoveryRequest>;
    }, TContext>;
    request?: SecondParameter<typeof customFetch>;
}) => UseMutationResult<Awaited<ReturnType<typeof discoverBulkVendors>>, TError, {
    data: BodyType<VendorDiscoveryRequest>;
}, TContext>;
export declare const getGetVendorComparisonUrl: (purchaseRequestId: number) => string;
/**
 * @summary Compare vendors for a purchase request
 */
export declare const getVendorComparison: (purchaseRequestId: number, options?: Parameters<typeof customFetch>[1]) => Promise<VendorComparison>;
export declare const getGetVendorComparisonQueryKey: (purchaseRequestId: number) => readonly [`/api/v1/vendor-comparisons/${number}`];
export declare const getGetVendorComparisonQueryOptions: <TData = Awaited<ReturnType<typeof getVendorComparison>>, TError = ErrorType<unknown>>(purchaseRequestId: number, options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof getVendorComparison>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}) => UseQueryOptions<Awaited<ReturnType<typeof getVendorComparison>>, TError, TData> & {
    queryKey: QueryKey;
};
export type GetVendorComparisonQueryResult = NonNullable<Awaited<ReturnType<typeof getVendorComparison>>>;
export type GetVendorComparisonQueryError = ErrorType<unknown>;
/**
 * @summary Compare vendors for a purchase request
 */
export declare function useGetVendorComparison<TData = Awaited<ReturnType<typeof getVendorComparison>>, TError = ErrorType<unknown>>(purchaseRequestId: number, options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof getVendorComparison>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}): UseQueryResult<TData, TError> & {
    queryKey: QueryKey;
};
export declare const getGetDecisionTwinUrl: (purchaseRequestId: number) => string;
/**
 * @summary Simulate procurement outcomes
 */
export declare const getDecisionTwin: (purchaseRequestId: number, options?: Parameters<typeof customFetch>[1]) => Promise<DecisionTwin>;
export declare const getGetDecisionTwinQueryKey: (purchaseRequestId: number) => readonly [`/api/v1/decision-twin/${number}`];
export declare const getGetDecisionTwinQueryOptions: <TData = Awaited<ReturnType<typeof getDecisionTwin>>, TError = ErrorType<unknown>>(purchaseRequestId: number, options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof getDecisionTwin>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}) => UseQueryOptions<Awaited<ReturnType<typeof getDecisionTwin>>, TError, TData> & {
    queryKey: QueryKey;
};
export type GetDecisionTwinQueryResult = NonNullable<Awaited<ReturnType<typeof getDecisionTwin>>>;
export type GetDecisionTwinQueryError = ErrorType<unknown>;
/**
 * @summary Simulate procurement outcomes
 */
export declare function useGetDecisionTwin<TData = Awaited<ReturnType<typeof getDecisionTwin>>, TError = ErrorType<unknown>>(purchaseRequestId: number, options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof getDecisionTwin>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}): UseQueryResult<TData, TError> & {
    queryKey: QueryKey;
};
export declare const getListPurchaseOrdersUrl: () => string;
/**
 * @summary List purchase orders
 */
export declare const listPurchaseOrders: (options?: Parameters<typeof customFetch>[1]) => Promise<PurchaseOrder[]>;
export declare const getListPurchaseOrdersQueryKey: () => readonly ["/api/v1/purchase-orders"];
export declare const getListPurchaseOrdersQueryOptions: <TData = Awaited<ReturnType<typeof listPurchaseOrders>>, TError = ErrorType<unknown>>(options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof listPurchaseOrders>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}) => UseQueryOptions<Awaited<ReturnType<typeof listPurchaseOrders>>, TError, TData> & {
    queryKey: QueryKey;
};
export type ListPurchaseOrdersQueryResult = NonNullable<Awaited<ReturnType<typeof listPurchaseOrders>>>;
export type ListPurchaseOrdersQueryError = ErrorType<unknown>;
/**
 * @summary List purchase orders
 */
export declare function useListPurchaseOrders<TData = Awaited<ReturnType<typeof listPurchaseOrders>>, TError = ErrorType<unknown>>(options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof listPurchaseOrders>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}): UseQueryResult<TData, TError> & {
    queryKey: QueryKey;
};
export declare const getCreatePurchaseOrderUrl: () => string;
/**
 * @summary Create a purchase order
 */
export declare const createPurchaseOrder: (purchaseOrderInput: PurchaseOrderInput, options?: Parameters<typeof customFetch>[1]) => Promise<PurchaseOrder>;
export declare const getCreatePurchaseOrderMutationOptions: <TError = ErrorType<unknown>, TContext = unknown>(options?: {
    mutation?: UseMutationOptions<Awaited<ReturnType<typeof createPurchaseOrder>>, TError, {
        data: BodyType<PurchaseOrderInput>;
    }, TContext>;
    request?: SecondParameter<typeof customFetch>;
}) => UseMutationOptions<Awaited<ReturnType<typeof createPurchaseOrder>>, TError, {
    data: BodyType<PurchaseOrderInput>;
}, TContext>;
export type CreatePurchaseOrderMutationResult = NonNullable<Awaited<ReturnType<typeof createPurchaseOrder>>>;
export type CreatePurchaseOrderMutationBody = BodyType<PurchaseOrderInput>;
export type CreatePurchaseOrderMutationError = ErrorType<unknown>;
/**
* @summary Create a purchase order
*/
export declare const useCreatePurchaseOrder: <TError = ErrorType<unknown>, TContext = unknown>(options?: {
    mutation?: UseMutationOptions<Awaited<ReturnType<typeof createPurchaseOrder>>, TError, {
        data: BodyType<PurchaseOrderInput>;
    }, TContext>;
    request?: SecondParameter<typeof customFetch>;
}) => UseMutationResult<Awaited<ReturnType<typeof createPurchaseOrder>>, TError, {
    data: BodyType<PurchaseOrderInput>;
}, TContext>;
export declare const getGetPurchaseOrderUrl: (id: number) => string;
/**
 * @summary Get purchase order detail
 */
export declare const getPurchaseOrder: (id: number, options?: Parameters<typeof customFetch>[1]) => Promise<PurchaseOrderDetail>;
export declare const getGetPurchaseOrderQueryKey: (id: number) => readonly [`/api/v1/purchase-orders/${number}`];
export declare const getGetPurchaseOrderQueryOptions: <TData = Awaited<ReturnType<typeof getPurchaseOrder>>, TError = ErrorType<unknown>>(id: number, options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof getPurchaseOrder>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}) => UseQueryOptions<Awaited<ReturnType<typeof getPurchaseOrder>>, TError, TData> & {
    queryKey: QueryKey;
};
export type GetPurchaseOrderQueryResult = NonNullable<Awaited<ReturnType<typeof getPurchaseOrder>>>;
export type GetPurchaseOrderQueryError = ErrorType<unknown>;
/**
 * @summary Get purchase order detail
 */
export declare function useGetPurchaseOrder<TData = Awaited<ReturnType<typeof getPurchaseOrder>>, TError = ErrorType<unknown>>(id: number, options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof getPurchaseOrder>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}): UseQueryResult<TData, TError> & {
    queryKey: QueryKey;
};
export declare const getGetOrderTrackingUrl: () => string;
/**
 * @summary Get active order tracking
 */
export declare const getOrderTracking: (options?: Parameters<typeof customFetch>[1]) => Promise<TrackingItem[]>;
export declare const getGetOrderTrackingQueryKey: () => readonly ["/api/v1/order-tracking"];
export declare const getGetOrderTrackingQueryOptions: <TData = Awaited<ReturnType<typeof getOrderTracking>>, TError = ErrorType<unknown>>(options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof getOrderTracking>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}) => UseQueryOptions<Awaited<ReturnType<typeof getOrderTracking>>, TError, TData> & {
    queryKey: QueryKey;
};
export type GetOrderTrackingQueryResult = NonNullable<Awaited<ReturnType<typeof getOrderTracking>>>;
export type GetOrderTrackingQueryError = ErrorType<unknown>;
/**
 * @summary Get active order tracking
 */
export declare function useGetOrderTracking<TData = Awaited<ReturnType<typeof getOrderTracking>>, TError = ErrorType<unknown>>(options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof getOrderTracking>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}): UseQueryResult<TData, TError> & {
    queryKey: QueryKey;
};
export declare const getGetVendorPerformanceUrl: () => string;
/**
 * @summary Get vendor performance rankings
 */
export declare const getVendorPerformance: (options?: Parameters<typeof customFetch>[1]) => Promise<VendorPerformance[]>;
export declare const getGetVendorPerformanceQueryKey: () => readonly ["/api/v1/vendor-performance"];
export declare const getGetVendorPerformanceQueryOptions: <TData = Awaited<ReturnType<typeof getVendorPerformance>>, TError = ErrorType<unknown>>(options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof getVendorPerformance>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}) => UseQueryOptions<Awaited<ReturnType<typeof getVendorPerformance>>, TError, TData> & {
    queryKey: QueryKey;
};
export type GetVendorPerformanceQueryResult = NonNullable<Awaited<ReturnType<typeof getVendorPerformance>>>;
export type GetVendorPerformanceQueryError = ErrorType<unknown>;
/**
 * @summary Get vendor performance rankings
 */
export declare function useGetVendorPerformance<TData = Awaited<ReturnType<typeof getVendorPerformance>>, TError = ErrorType<unknown>>(options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof getVendorPerformance>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}): UseQueryResult<TData, TError> & {
    queryKey: QueryKey;
};
export declare const getGetAnalyticsUrl: () => string;
/**
 * @summary Get analytics
 */
export declare const getAnalytics: (options?: Parameters<typeof customFetch>[1]) => Promise<Analytics>;
export declare const getGetAnalyticsQueryKey: () => readonly ["/api/v1/analytics"];
export declare const getGetAnalyticsQueryOptions: <TData = Awaited<ReturnType<typeof getAnalytics>>, TError = ErrorType<unknown>>(options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof getAnalytics>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}) => UseQueryOptions<Awaited<ReturnType<typeof getAnalytics>>, TError, TData> & {
    queryKey: QueryKey;
};
export type GetAnalyticsQueryResult = NonNullable<Awaited<ReturnType<typeof getAnalytics>>>;
export type GetAnalyticsQueryError = ErrorType<unknown>;
/**
 * @summary Get analytics
 */
export declare function useGetAnalytics<TData = Awaited<ReturnType<typeof getAnalytics>>, TError = ErrorType<unknown>>(options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof getAnalytics>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}): UseQueryResult<TData, TError> & {
    queryKey: QueryKey;
};
export declare const getListNotificationsUrl: () => string;
/**
 * @summary List notifications
 */
export declare const listNotifications: (options?: Parameters<typeof customFetch>[1]) => Promise<Notification[]>;
export declare const getListNotificationsQueryKey: () => readonly ["/api/v1/notifications"];
export declare const getListNotificationsQueryOptions: <TData = Awaited<ReturnType<typeof listNotifications>>, TError = ErrorType<unknown>>(options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof listNotifications>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}) => UseQueryOptions<Awaited<ReturnType<typeof listNotifications>>, TError, TData> & {
    queryKey: QueryKey;
};
export type ListNotificationsQueryResult = NonNullable<Awaited<ReturnType<typeof listNotifications>>>;
export type ListNotificationsQueryError = ErrorType<unknown>;
/**
 * @summary List notifications
 */
export declare function useListNotifications<TData = Awaited<ReturnType<typeof listNotifications>>, TError = ErrorType<unknown>>(options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof listNotifications>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}): UseQueryResult<TData, TError> & {
    queryKey: QueryKey;
};
export declare const getMarkAllNotificationsReadUrl: () => string;
/**
 * @summary Mark notifications read
 */
export declare const markAllNotificationsRead: (options?: Parameters<typeof customFetch>[1]) => Promise<Notification[]>;
export declare const getMarkAllNotificationsReadMutationOptions: <TError = ErrorType<unknown>, TContext = unknown>(options?: {
    mutation?: UseMutationOptions<Awaited<ReturnType<typeof markAllNotificationsRead>>, TError, void, TContext>;
    request?: SecondParameter<typeof customFetch>;
}) => UseMutationOptions<Awaited<ReturnType<typeof markAllNotificationsRead>>, TError, void, TContext>;
export type MarkAllNotificationsReadMutationResult = NonNullable<Awaited<ReturnType<typeof markAllNotificationsRead>>>;
export type MarkAllNotificationsReadMutationError = ErrorType<unknown>;
/**
* @summary Mark notifications read
*/
export declare const useMarkAllNotificationsRead: <TError = ErrorType<unknown>, TContext = unknown>(options?: {
    mutation?: UseMutationOptions<Awaited<ReturnType<typeof markAllNotificationsRead>>, TError, void, TContext>;
    request?: SecondParameter<typeof customFetch>;
}) => UseMutationResult<Awaited<ReturnType<typeof markAllNotificationsRead>>, TError, void, TContext>;
export declare const getChatWithAssistantUrl: () => string;
/**
 * @summary Ask AQURA Assistant
 */
export declare const chatWithAssistant: (chatInput: ChatInput, options?: Parameters<typeof customFetch>[1]) => Promise<ChatResponse>;
export declare const getChatWithAssistantMutationOptions: <TError = ErrorType<unknown>, TContext = unknown>(options?: {
    mutation?: UseMutationOptions<Awaited<ReturnType<typeof chatWithAssistant>>, TError, {
        data: BodyType<ChatInput>;
    }, TContext>;
    request?: SecondParameter<typeof customFetch>;
}) => UseMutationOptions<Awaited<ReturnType<typeof chatWithAssistant>>, TError, {
    data: BodyType<ChatInput>;
}, TContext>;
export type ChatWithAssistantMutationResult = NonNullable<Awaited<ReturnType<typeof chatWithAssistant>>>;
export type ChatWithAssistantMutationBody = BodyType<ChatInput>;
export type ChatWithAssistantMutationError = ErrorType<unknown>;
/**
* @summary Ask AQURA Assistant
*/
export declare const useChatWithAssistant: <TError = ErrorType<unknown>, TContext = unknown>(options?: {
    mutation?: UseMutationOptions<Awaited<ReturnType<typeof chatWithAssistant>>, TError, {
        data: BodyType<ChatInput>;
    }, TContext>;
    request?: SecondParameter<typeof customFetch>;
}) => UseMutationResult<Awaited<ReturnType<typeof chatWithAssistant>>, TError, {
    data: BodyType<ChatInput>;
}, TContext>;
export {};
//# sourceMappingURL=api.d.ts.map