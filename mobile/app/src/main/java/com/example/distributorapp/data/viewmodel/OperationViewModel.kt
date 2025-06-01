package com.example.distributorapp.data.viewmodel

import android.util.Log
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.distributorapp.data.UserPreferences
import com.example.distributorapp.data.model.Operation
import com.example.distributorapp.data.repository.OperationRepository
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch

class OperationViewModel(
    private val userPreferences: UserPreferences,
    private val repository: OperationRepository
): ViewModel() {
    private val _operations = MutableStateFlow<List<Operation>>(emptyList())
    val operations: StateFlow<List<Operation>> get() = _operations

    private val _isLoading = MutableStateFlow(false)
    val isLoading: StateFlow<Boolean> get() = _isLoading

    fun fetchOperations(
        page: Int,
        limit: Int,
        partner_name: String?,
        good_name: String?,
        oper_name: String?,
        start_date: String?,
        end_date: String?
    ) {
        viewModelScope.launch {
            _isLoading.value = true

            try {
                val token = userPreferences.getToken()
                token?.let {
                    val response = repository.getOperations(
                        it,
                        page,
                        limit,
                        partner_name,
                        good_name,
                        oper_name,
                        start_date,
                        end_date
                    )
                    if (response.isSuccessful) {
                        _operations.value = response.body()?.operations ?: emptyList()
                    }
                } ?: run {
                    Log.e("OperationViewModel", "Token is null")
                    _operations.value = emptyList()
                }
            } catch (e: Exception) {
                Log.e("OperationViewModel", "Exception when fetching Operations", e)
                _operations.value = emptyList()
            } finally {
                _isLoading.value = false
            }

        }
    }
}