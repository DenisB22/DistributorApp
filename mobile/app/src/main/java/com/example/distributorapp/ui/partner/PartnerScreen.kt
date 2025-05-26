package com.example.distributorapp.ui.partner

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.example.distributorapp.data.UserPreferences
import com.example.distributorapp.viewmodel.PartnerViewModel
import com.example.distributorapp.viewmodel.PartnerViewModelFactory
import androidx.compose.ui.Alignment
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import com.example.distributorapp.ui.components.MainScaffoldLayout
import com.example.distributorapp.ui.navigation.DrawerItem
import androidx.navigation.NavController


@Composable
fun PartnerList(viewModel: PartnerViewModel) {
    val partners by viewModel.partners.collectAsState()
    val isLoading by viewModel.isLoading.collectAsState()

    if (isLoading) {
        Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
            CircularProgressIndicator()
        }
    } else {
        if (partners.isEmpty()) {
            Text(
                text = "Няма намерени партньори",
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
                items(partners) { partner ->
                    Card(
                        modifier = Modifier.fillMaxWidth(),
                        elevation = CardDefaults.cardElevation(4.dp)
                    ) {
                        Column(modifier = Modifier.padding(12.dp)) {
                            Text(text = "Фирма: ${partner.company}")
                            Text(text = "Телефон: ${partner.phone}")
                            Text(text = "Булстат: ${partner.taxNo}")
                        }
                    }
                }
            }
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun PartnerScreen(
    userPreferences: UserPreferences,
    onLogout: () -> Unit,
    navController: NavController
) {
    val viewModel: PartnerViewModel = viewModel(
        factory = PartnerViewModelFactory(userPreferences)
    )

    LaunchedEffect(Unit) {
        viewModel.searchPartners(field="", query = "")
    }

    val searchOptions = mapOf(
        "Фирма" to "company",
        "МОЛ" to "mol",
        "Телефон" to "phone",
        "Булстат" to "tax_no"
    )

    var selectedOption by remember { mutableStateOf("Фирма") }
    var searchText by remember { mutableStateOf("") }

    val drawerItems = listOf(
        DrawerItem(title = "Dashboard", route = "dashboard_screen"),
        DrawerItem(title = "Partners", route = "partner_screen"),
        DrawerItem(title = "Products", route = "product_screen"),
        // We will add another screens here
    )

    MainScaffoldLayout(
        navController = navController,
        drawerItems = drawerItems,
        onLogout = onLogout,
        screenTitle = "Партньори"
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
                viewModel.searchPartners(
                    searchOptions[selectedOption] ?: "company",
                    searchText
                )
            }) {
                Text("Търси")
            }

            PartnerList(viewModel)
        }
    }
}