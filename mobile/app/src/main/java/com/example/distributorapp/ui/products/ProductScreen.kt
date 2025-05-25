package com.example.distributorapp.ui.products

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
import com.example.distributorapp.data.repository.ProductRepository
import com.example.distributorapp.data.viewmodel.ProductViewModel
import com.example.distributorapp.data.viewmodel.ProductViewModelFactory


@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ProductScreen(
    userPreferences: UserPreferences,
    navController: NavController,
    onLogout: () -> Unit
) {
    val api = RetrofitClient.createProductApi(userPreferences)
    val repository = ProductRepository(api)
    val factory = remember { ProductViewModelFactory(repository, userPreferences) }
    val viewModel: ProductViewModel = viewModel(factory = factory)

    val drawerItems = listOf(
        DrawerItem(title = "Dashboard", route = "dashboard_screen"),
        DrawerItem(title = "Partners", route = "partner_screen"),
        DrawerItem(title = "Products", route = "product_screen"),
        // We will add another screens here
    )

    val searchOptions = mapOf(
        "Име" to "name",
        "Код" to "code",
        "Баркод" to "barcode"
    )

    var selectedOption by remember { mutableStateOf("Име") }
    var searchText by remember { mutableStateOf("") }
    val isLoading by viewModel.isLoading.collectAsState()
    val products by viewModel.products.collectAsState()

    MainScaffoldLayout(
        navController = navController,
        drawerItems = drawerItems,
        onLogout = onLogout,
        screenTitle = "Продукти"
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
                val selectedField = searchOptions[selectedOption] ?: "name"
                val name = if (selectedField == "name") searchText else null
                val code = if (selectedField == "code") searchText else null
                val barcode = if (selectedField == "barcode") searchText else null

                viewModel.searchProducts(
                    name = name,
                    code = code,
                    barcode = barcode,
                    field = selectedField,
                    query = searchText
                )
            }) {
                Text(text = "Търси")
            }

            if (isLoading) {
                Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                    CircularProgressIndicator()
                }
            } else {
                if (products.isEmpty()) {
                    Text("Няма намерени продукти")
                } else {
                    LazyColumn(
                        verticalArrangement = Arrangement.spacedBy(8.dp),
                        modifier = Modifier
                            .fillMaxSize()
                            .padding(top = 16.dp)
                    ) {
                        items(products) { product ->
                            Card(
                                modifier = Modifier.fillMaxWidth(),
                                elevation = CardDefaults.cardElevation(4.dp)
                            ) {
                                Column(modifier = Modifier.padding(12.dp)) {
                                    Text("Име: ${product.Name}")
                                    Text("Код: ${product.Code}")
                                    Text("Баркод: ${product.BarCode}")
                                    Text("Цена: ${product.PriceOut} лв")
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}

