package com.example.distributorapp

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.foundation.layout.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.compose.ui.tooling.preview.Preview
import com.example.distributorapp.ui.theme.DistributorAppTheme
import com.example.distributorapp.data.UserPreferences
import kotlinx.coroutines.runBlocking
import androidx.lifecycle.lifecycleScope
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.launch


class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        val userPreferences = UserPreferences(this)

        setContent {
            val isLoggedIn by userPreferences.isLoggedIn.collectAsState(initial = false)

            DistributorAppTheme {
                if (isLoggedIn) {
                    DashboardScreen(userPreferences = userPreferences)
                } else {
                    LoginScreen(
                        onLoginSuccess = {
                            lifecycleScope.launch {
                                userPreferences.setLoggedIn(true)
                            }
                        }
                    )
                }
            }
        }
    }
}

@Composable
fun DashboardScreen(userPreferences: UserPreferences) {
    val coroutineScope = rememberCoroutineScope()

    Scaffold(
        content = { paddingValues ->
            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(paddingValues)
                    .padding(16.dp),
                verticalArrangement = Arrangement.Center,
                horizontalAlignment = Alignment.CenterHorizontally
            ) {
                Text(text = "Добре дошли в приложението!")

                Spacer(modifier = Modifier.height(16.dp))

                Button(
                    onClick = {
                        coroutineScope.launch {
                            userPreferences.setLoggedIn(false) // Запазва излизането
                        }
                    }
                ) {
                    Text("Изход")
                }
            }
        }
    )
}

@Preview(showBackground = true)
@Composable
fun DefaultPreview() {
    DistributorAppTheme {
        LoginScreen(onLoginSuccess = {})
    }
}
