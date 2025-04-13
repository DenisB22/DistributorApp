package com.example.distributorapp.data

import android.content.Context
import androidx.datastore.preferences.core.booleanPreferencesKey
import androidx.datastore.preferences.core.stringPreferencesKey
import androidx.datastore.preferences.core.edit
import androidx.datastore.preferences.preferencesDataStore
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.flow.map
import android.util.Log

private val Context.dataStore by preferencesDataStore(name = "user_prefs")

class UserPreferences(private val context: Context) {

    companion object {
        private val IS_LOGGED_IN_KEY = booleanPreferencesKey("is_logged_in")
        private val AUTH_TOKEN_KEY = stringPreferencesKey("auth_token")
    }

    val isLoggedIn: Flow<Boolean> = context.dataStore.data
        .map { preferences ->
            preferences[IS_LOGGED_IN_KEY] ?: false
        }

    suspend fun setLoggedIn(isLoggedIn: Boolean) {
        context.dataStore.edit { preferences ->
            preferences[IS_LOGGED_IN_KEY] = isLoggedIn
        }
    }

    suspend fun saveToken(token: String) {
        Log.d("UserPreferences", "Saving token: $token")
        context.dataStore.edit { preferences ->
            preferences[AUTH_TOKEN_KEY] = token
        }
    }

    suspend fun getToken(): String? {
        val token = context.dataStore.data
            .map { it[AUTH_TOKEN_KEY] }
            .first()

        Log.d("UserPreferences", "Retrieved token: $token")

        return token
    }

    suspend fun clearToken() {
        context.dataStore.edit { preferences ->
            preferences.remove(AUTH_TOKEN_KEY)
        }
    }

    suspend fun hasToken(): Boolean {
        return getToken()?.isNotEmpty() == true
    }
}