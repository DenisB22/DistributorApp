package com.example.distributorapp.ui.dashboard

import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.example.distributorapp.data.UserPreferences
import com.example.distributorapp.data.model.DashboardResponse
import com.example.distributorapp.viewmodel.DashboardViewModel
import com.example.distributorapp.viewmodel.DashboardViewModelFactory

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun DashboardScreen(
    userPreferences: UserPreferences,
    onLogout: () -> Unit
) {
    val viewModel: DashboardViewModel = viewModel(
        factory = DashboardViewModelFactory(userPreferences)
    )

    val dashboardData by viewModel.dashboardData.collectAsState()
    val isLoading by viewModel.isLoading.collectAsState()

    LaunchedEffect(Unit) {
        viewModel.fetchDashboardData()
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Dashboard") },
                actions = {
                    Button(onClick = onLogout) {
                        Text("Logout")
                    }
                }
            )
        }
    ) { paddingValues ->
        Box(
            modifier = Modifier
                .padding(paddingValues)
                .fillMaxSize()
        ) {
            when {
                isLoading -> {
                    CircularProgressIndicator(modifier = Modifier.align(Alignment.Center))
                }

                dashboardData != null -> {
                    DashboardContent(dashboardData!!)
                }

                else -> {
                    Text("No data available", modifier = Modifier.align(Alignment.Center))
                }
            }
        }
    }
}

@Composable
fun DashboardContent(data: DashboardResponse) {
    Column(modifier = Modifier
        .padding(16.dp)
        .fillMaxWidth()) {

        Text(text = "Total Sales: ${data.totalSales}")
        Text(text = "Total Quantity: ${data.totalQuantity}")
        Text(text = "Total Revenue: ${data.totalRevenue} лв")

        Spacer(modifier = Modifier.height(16.dp))

        data.topPartner?.let {
            Text(text = "Top Partner: ${it.name} (${it.total} лв)")
        }

        data.topGood?.let {
            Text(text = "Top Product: ${it.name} (${it.total} лв)")
        }

        Spacer(modifier = Modifier.height(24.dp))

        Text("Recent Operations:", style = MaterialTheme.typography.titleMedium)
        data.recentOperations.forEach { op ->
            Text("- ${op.operationName}: ${op.priceOut} лв x ${op.operationQtty}")
        }
    }
}
