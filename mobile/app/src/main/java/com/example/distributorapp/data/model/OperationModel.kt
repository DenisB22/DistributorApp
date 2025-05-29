package com.example.distributorapp.data.model

import com.google.gson.annotations.SerializedName


data class OperationsResponse(
    @SerializedName("operations") val operations: List<Operation>
)


data class Operation(
    @SerializedName("operation_id") val operationId: Int,
    @SerializedName("operation_name") val operationName: String?,
    @SerializedName("good_name") val goodName: String?,
    @SerializedName("operation_qtty") val operationQtty: Double?,
    @SerializedName("price_in") val priceIn: Double?,
    @SerializedName("price_out") val priceOut: Double?,
    @SerializedName("operation_date") val operationDate: String?,
)
