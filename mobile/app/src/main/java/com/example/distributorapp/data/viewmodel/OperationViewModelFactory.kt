package com.example.distributorapp.data.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import com.example.distributorapp.data.UserPreferences
import com.example.distributorapp.data.repository.OperationRepository

class OperationViewModelFactory(
    private val repository: OperationRepository,
    private val userPreferences: UserPreferences
) : ViewModelProvider.Factory {
    override fun <T : ViewModel> create(modelClass: Class<T>): T {
        if (modelClass.isAssignableFrom(OperationViewModel::class.java)) {
            return OperationViewModel(userPreferences, repository) as T
        }
        throw IllegalArgumentException("Unknown ViewModel class")
    }
}