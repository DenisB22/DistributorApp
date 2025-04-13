package com.example.distributorapp.ui.dashboard

import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.compose.foundation.verticalScroll
import androidx.compose.foundation.rememberScrollState
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
    Column(
        modifier = Modifier
            .padding(16.dp)
            .fillMaxSize()
            .verticalScroll(rememberScrollState()),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {

        Card(
            modifier = Modifier.fillMaxWidth(),
            elevation = CardDefaults.cardElevation(4.dp)
        ) {
            Column(modifier = Modifier.padding(16.dp)) {
                Text(text = "Total Sales: ${data.totalSales}")
                Text(text = "Total Quantity: ${data.totalQuantity}")
                Text(text = "Total Revenue: ${data.totalRevenue} лв")
            }
        }

        Card(
            modifier = Modifier.fillMaxWidth(),
            elevation = CardDefaults.cardElevation(4.dp)
        ) {
            Column(modifier = Modifier.padding(16.dp)) {
                data.topPartner?.let {
                    Text(text = "Top Partner: ${it.name} (${it.total} лв)")
                }
                data.topGood?.let {
                    Text(text = "Top Product: ${it.name} (${it.total} лв)")
                }
            }
        }

        Text(
            text = "Recent Operations:",
            style = MaterialTheme.typography.titleMedium
        )

        data.recentOperations.forEach { op ->
            Card(
                modifier = Modifier.fillMaxWidth(),
                elevation = CardDefaults.cardElevation(2.dp)
            ) {
                Column(modifier = Modifier.padding(12.dp)) {
                    Text(text = "Operation: ${op.operationName}")
                    Text(text = "Partner: ${op.partnerName}")
                    Text(text = "Product: ${op.goodName}")
                    Text(text = "Quantity: ${op.operationQtty}")
                    Text(text = "Unit Price: ${op.priceOut} лв")
                    Text(text = "Total Price: ${"%.2f".format(op.priceOut * op.operationQtty)} лв")
                    Text(text = "Date: ${op.operationDate.take(10)}")
                }
            }
        }
    }
}
