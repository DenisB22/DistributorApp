package com.example.distributorapp.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.distributorapp.data.UserPreferences
import com.example.distributorapp.data.model.Partner
import com.example.distributorapp.data.repository.PartnerRepository
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch

class PartnerViewModel(
    private val userPreferences: UserPreferences,
    private val repository: PartnerRepository
) : ViewModel() {

    private val _partners = MutableStateFlow<List<Partner>>(emptyList())
    val partners: StateFlow<List<Partner>> = _partners

    private val _isLoading = MutableStateFlow(false)
    val isLoading: StateFlow<Boolean> = _isLoading

    fun fetchPartners(
        token: String?,
        page: Int,
        limit: Int,
        company: String?,
        mol: String?,
        phone: String?,
        tax_no: String?
    ) {
        viewModelScope.launch {
            _isLoading.value = true
            try {
                val token = userPreferences.getToken()
                val response = repository.getPartners(token, page, limit, company, mol, phone, tax_no)
                if (response.isSuccessful) {
                    _partners.value = response.body()?.partners ?: emptyList()
                } else {
                    _partners.value = emptyList()
                }
            } catch (e: Exception) {
                _partners.value = emptyList()
            } finally {
                _isLoading.value = false
            }
        }
    }

    fun searchPartners(field: String, query: String) {
        viewModelScope.launch {
            _isLoading.value = true
            try {
                val token = userPreferences.getToken()

                val response = repository.getPartners(
                    token = token,
                    page = 1,
                    limit = 20,
                    company = if (field == "company") query else null,
                    mol = if (field == "mol") query else null,
                    phone = if (field == "phone") query else null,
                    tax_no = if (field == "tax_no") query else null
                )

                if (response.isSuccessful) {
                    _partners.value = response.body()?.partners ?: emptyList()
                } else {
                    _partners.value = emptyList()
                }
            } catch (e: Exception) {
                _partners.value = emptyList()
            } finally {
                _isLoading.value = false
            }
        }
    }
}