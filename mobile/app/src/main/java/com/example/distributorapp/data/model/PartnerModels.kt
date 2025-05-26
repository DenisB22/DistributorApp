package com.example.distributorapp.data.model

import com.google.gson.annotations.SerializedName

data class PartnerResponse(
    @SerializedName("partners") val partners: List<Partner>
)

data class Partner(
    @SerializedName("partner_id") val partnerId: Int,
    @SerializedName("company") val company: String?,
    @SerializedName("mol") val mol: String?,
    @SerializedName("phone") val phone: String?,
    @SerializedName("tax_no") val taxNo: String?
)