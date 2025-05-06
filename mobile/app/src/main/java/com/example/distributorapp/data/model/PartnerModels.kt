package com.example.distributorapp.data.model

import com.google.gson.annotations.SerializedName

data class PartnerResponse(
    @SerializedName("partners") val partners: List<Partner>
)

data class Partner(
    val ID: Int,
    val Company: String?,
    val MOL: String?,
    val Phone: String?,
    val TaxNo: String?
)