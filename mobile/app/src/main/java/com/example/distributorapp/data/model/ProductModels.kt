package com.example.distributorapp.data.model

import com.google.gson.annotations.SerializedName


data class ProductResponse(
    @SerializedName("products") val products: List<Product>
)


data class Product(
    @SerializedName("product_id") val productId: Int,
    @SerializedName("code") val code: String?,
    @SerializedName("bar_code") val barCode: String?,
    @SerializedName("name") val name: String?,
    @SerializedName("measure") val measure: String?,
    @SerializedName("price_out") val priceOut: Double?,
    @SerializedName("description") val description: String?
)