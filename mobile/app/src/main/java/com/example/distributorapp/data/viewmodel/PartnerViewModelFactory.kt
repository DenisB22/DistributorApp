package com.example.distributorapp.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import com.example.distributorapp.data.RetrofitClient
import com.example.distributorapp.data.UserPreferences
import com.example.distributorapp.data.repository.PartnerRepository

class PartnerViewModelFactory(
    private val userPreferences: UserPreferences
) : ViewModelProvider.Factory {
    override fun <T : ViewModel> create(modelClass: Class<T>): T {
        if (modelClass.isAssignableFrom(PartnerViewModel::class.java)) {
            val api = RetrofitClient.createPartnerApi(userPreferences)
            val repository = PartnerRepository(api)
            return PartnerViewModel(userPreferences, repository) as T
        }
        throw IllegalArgumentException("Unknown ViewModel class")
    }
}