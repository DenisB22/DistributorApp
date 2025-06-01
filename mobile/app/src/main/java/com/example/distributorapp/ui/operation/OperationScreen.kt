package com.example.distributorapp.ui.operation

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.example.distributorapp.data.UserPreferences
import androidx.compose.ui.Alignment
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import com.example.distributorapp.ui.components.MainScaffoldLayout
import com.example.distributorapp.ui.navigation.DrawerItem
import androidx.navigation.NavController
import com.example.distributorapp.data.RetrofitClient
import com.example.distributorapp.data.repository.OperationRepository
import com.example.distributorapp.data.viewmodel.OperationViewModel
import com.example.distributorapp.data.viewmodel.OperationViewModelFactory


@Composable
fun OperationList(viewModel: OperationViewModel) {
    val operations by viewModel.operations.collectAsState()
    val isLoading by viewModel.isLoading.collectAsState()

    if (isLoading) {
        Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
            CircularProgressIndicator()
        }
    } else {
        if (operations.isEmpty()) {
            Text(
                text = "Няма намерени операции",
                modifier = Modifier.padding(16.dp)
            )
        } else {
            // SCROLLABLE COLUMN
            LazyColumn(
                verticalArrangement = Arrangement.spacedBy(8.dp),
                modifier = Modifier
                    .fillMaxSize()
                    .padding(16.dp)
            ) {
                items(operations) { operation ->
                    Card(
                        modifier = Modifier.fillMaxWidth(),
                        elevation = CardDefaults.cardElevation(4.dp)
                    ) {
                        Column(modifier = Modifier.padding(12.dp)) {
                            Text(text = "Име на операция: ${operation.operationName}")
                            Text(text = "Име на продукт: ${operation.goodName}")
                            Text(text = "Количество на операцията: ${operation.operationQtty}")
                            Text(text = "Доставна цена: ${operation.priceIn}")
                            Text(text = "Продажна цена: ${operation.priceOut}")
                        }
                    }
                }
            }
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun OperationScreen(
    userPreferences: UserPreferences,
    onLogout: () -> Unit,
    navController: NavController
) {

    val api = RetrofitClient.createOperationApi(userPreferences)
    val repository = OperationRepository(api)

    val viewModel: OperationViewModel = viewModel(
        factory = OperationViewModelFactory(repository, userPreferences)
    )

    LaunchedEffect(Unit) {
        viewModel.fetchOperations(
            page=1,
            limit=20,
            partner_name="",
            good_name="",
            oper_name="",
            start_date="",
            end_date=""
        )
    }

    val searchOptions = mapOf(
        "Име на партньор" to "partner_name",
        "Име на стока" to "good_name",
        "Име на операция" to "oper_name",
        "Стартова дата" to "start_date",
        "Крайна дата" to "end_date"
    )

    var selectedOption by remember { mutableStateOf("Име на партньор") }
    var searchText by remember { mutableStateOf("") }

    val drawerItems = listOf(
        DrawerItem(title = "Dashboard", route = "dashboard_screen"),
        DrawerItem(title = "Partners", route = "partner_screen"),
        DrawerItem(title = "Products", route = "product_screen"),
        DrawerItem(title = "Operations", route = "operation_screen"),
        // We will add another screens here
    )

    MainScaffoldLayout(
        navController = navController,
        drawerItems = drawerItems,
        onLogout = onLogout,
        screenTitle = "Операции"
    ) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            var expanded by remember { mutableStateOf(false) }
            ExposedDropdownMenuBox(
                expanded = expanded,
                onExpandedChange = { expanded = !expanded }
            ) {
                TextField(
                    value = selectedOption,
                    onValueChange = {},
                    readOnly = true,
                    label = { Text("Търси по") },
                    trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expanded = expanded) },
                    modifier = Modifier.menuAnchor()
                )

                ExposedDropdownMenu(
                    expanded = expanded,
                    onDismissRequest = { expanded = false }
                ) {
                    searchOptions.keys.forEach { option ->
                        DropdownMenuItem(
                            text = { Text(option) },
                            onClick = {
                                selectedOption = option
                                expanded = false
                            }
                        )
                    }
                }
            }

            TextField(
                value = searchText,
                onValueChange = { searchText = it },
                label = { Text("Стойност за търсене") },
                keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Text),
                modifier = Modifier.fillMaxWidth()
            )

            Button(onClick = {
                val selectedField = searchOptions[selectedOption] ?: "partner_id"
                val partner_name = if (selectedField == "partner_name") searchText else null
                val good_name = if (selectedField == "good_name") searchText  else null
                val oper_name = if (selectedField == "oper_name") searchText  else null
                val start_date = if (selectedField == "start_date") searchText else null
                val end_date = if (selectedField == "end_date") searchText else null

                viewModel.fetchOperations(
                    1,
                    20,
                    partner_name,
                    good_name,
                    oper_name,
                    start_date,
                    end_date
                )
            }) {
                Text("Търси")
            }

            OperationList(viewModel)
        }
    }
}