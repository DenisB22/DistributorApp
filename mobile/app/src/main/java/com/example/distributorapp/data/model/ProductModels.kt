package com.example.distributorapp.data.model

import com.google.gson.annotations.SerializedName


data class ProductResponse(
    @SerializedName("products") val products: List<Product>
)


data class Product(
    val ID: Int,
    val Code: String,
    val BarCode: String?,
    val Name: String,
    val Measure: String,
    val PriceIn: Double,
    val PriceOut: Double,
    val Description: String?
)