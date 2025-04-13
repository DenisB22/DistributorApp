package com.example.distributorapp.data.model

import com.google.gson.annotations.SerializedName

data class DashboardResponse(
    @SerializedName("total_sales") val totalSales: Int,
    @SerializedName("total_quantity") val totalQuantity: Float,
    @SerializedName("total_revenue") val totalRevenue: Float,
    @SerializedName("top_partner") val topPartner: TopEntity?,
    @SerializedName("top_good") val topGood: TopEntity?,
    @SerializedName("recent_operations") val recentOperations: List<OperationResponse>
)

data class TopEntity(
    @SerializedName("id") val id: Int,
    @SerializedName("name") val name: String,
    @SerializedName("total") val total: Float
)

data class OperationResponse(
    @SerializedName("operation_id") val operationId: Int,
    @SerializedName("operation_type") val operationType: Int,
    @SerializedName("operation_name") val operationName: String,
    @SerializedName("operation_date") val operationDate: String,
    @SerializedName("operation_qtty") val operationQtty: Float,
    @SerializedName("user_id") val userId: Int,
    @SerializedName("user_name") val userName: String,
    @SerializedName("partner_id") val partnerId: Int?,
    @SerializedName("partner_name") val partnerName: String?,
    @SerializedName("good_id") val goodId: Int?,
    @SerializedName("good_name") val goodName: String?,
    @SerializedName("price_out") val priceOut: Float,
    @SerializedName("price_in") val priceIn: Float?
)