package com.transferapp.filetransfer

import android.Manifest
import android.content.ClipboardManager
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.net.Uri
import android.os.Build
import android.os.Bundle
import android.view.View
import android.widget.Toast
import androidx.activity.result.contract.ActivityResultContracts
import androidx.appcompat.app.AlertDialog
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.ContextCompat
import androidx.recyclerview.widget.LinearLayoutManager
import com.transferapp.filetransfer.adapter.HistoryAdapter
import com.transferapp.filetransfer.data.ItemType
import com.transferapp.filetransfer.data.TransferItem
import com.transferapp.filetransfer.databinding.ActivityMainBinding
import com.transferapp.filetransfer.network.RetrofitClient
import com.transferapp.filetransfer.network.TextRequest
import kotlinx.coroutines.*
import okhttp3.MediaType.Companion.toMediaTypeOrNull
import okhttp3.MultipartBody
import okhttp3.RequestBody.Companion.asRequestBody
import java.io.File

class MainActivity : AppCompatActivity() {

    private lateinit var binding: ActivityMainBinding
    private val historyList = mutableListOf<TransferItem>()
    private lateinit var historyAdapter: HistoryAdapter
    
    private var serverIp = "192.168.1.100"
    private var isConnected = false
    
    private val scope = CoroutineScope(Dispatchers.Main + Job())
    
    // 文件选择器
    private val filePickerLauncher = registerForActivityResult(
        ActivityResultContracts.GetContent()
    ) { uri: Uri? ->
        uri?.let { uploadFile(it) }
    }
    
    // 图片选择器
    private val imagePickerLauncher = registerForActivityResult(
        ActivityResultContracts.GetContent()
    ) { uri: Uri? ->
        uri?.let { uploadImage(it) }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)
        
        setupUI()
        setupClickListeners()
        checkPermissions()
        
        // 处理系统分享的内容
        handleShareIntent(intent)
    }
    
    override fun onNewIntent(intent: Intent?) {
        super.onNewIntent(intent)
        handleShareIntent(intent)
    }
    
    private fun setupUI() {
        // 设置RecyclerView
        historyAdapter = HistoryAdapter(historyList) { item ->
            showToast("已选择: ${item.fileName}")
        }
        binding.rvHistory.layoutManager = LinearLayoutManager(this)
        binding.rvHistory.adapter = historyAdapter
        
        // 设置默认IP
        binding.etServerIp.setText(serverIp)
    }
    
    private fun setupClickListeners() {
        // 连接服务器
        binding.btnConnect.setOnClickListener {
            val ip = binding.etServerIp.text.toString().trim()
            if (ip.isNotEmpty()) {
                connectToServer(ip)
            } else {
                showToast("请输入服务器IP地址")
            }
        }
        
        // 发送文本
        binding.btnSendText.setOnClickListener {
            showTextInputDialog()
        }
        
        // 发送图片
        binding.btnSendImage.setOnClickListener {
            if (!checkConnection()) return@setOnClickListener
            imagePickerLauncher.launch("image/*")
        }
        
        // 发送文件
        binding.btnSendFile.setOnClickListener {
            if (!checkConnection()) return@setOnClickListener
            filePickerLauncher.launch("*/*")
        }
        
        // 从剪贴板粘贴
        binding.btnPasteClipboard.setOnClickListener {
            pasteFromClipboard()
        }
    }
    
    private fun connectToServer(ip: String) {
        scope.launch {
            try {
                binding.btnConnect.isEnabled = false
                binding.btnConnect.text = "连接中..."
                
                RetrofitClient.setBaseUrl(ip)
                val response = RetrofitClient.apiService.getDeviceInfo()
                
                if (response.isSuccessful && response.body()?.success == true) {
                    isConnected = true
                    serverIp = ip
                    binding.tvConnectionStatus.text = "🟢 已连接到 ${response.body()?.device_name}"
                    binding.tvConnectionStatus.setTextColor(ContextCompat.getColor(this@MainActivity, R.color.success))
                    showToast("✅ 连接成功！")
                } else {
                    throw Exception("连接失败")
                }
            } catch (e: Exception) {
                isConnected = false
                binding.tvConnectionStatus.text = "🔴 连接失败"
                binding.tvConnectionStatus.setTextColor(ContextCompat.getColor(this@MainActivity, R.color.error))
                showToast("❌ 连接失败: ${e.message}")
            } finally {
                binding.btnConnect.isEnabled = true
                binding.btnConnect.text = "🔗 连接服务器"
            }
        }
    }
    
    private fun uploadFile(uri: Uri) {
        if (!checkConnection()) return
        
        scope.launch {
            try {
                showProgress(true)
                
                val fileName = getFileName(uri) ?: "unknown_file"
                val inputStream = contentResolver.openInputStream(uri)
                val bytes = inputStream?.readBytes()
                inputStream?.close()
                
                if (bytes == null) throw Exception("无法读取文件")
                
                val requestBody = bytes.toRequestBody(null)
                val multipartBody = MultipartBody.Part.createFormData(
                    "file",
                    fileName,
                    requestBody
                )
                
                val response = RetrofitClient.apiService.uploadFile(multipartBody)
                
                if (response.isSuccessful && response.body()?.success == true) {
                    addToHistory(ItemType.FILE, fileName, bytes.size.toLong())
                    showToast("✅ 文件上传成功！")
                } else {
                    throw Exception(response.body()?.message ?: "上传失败")
                }
            } catch (e: Exception) {
                showToast("❌ 上传失败: ${e.message}")
                addToHistory(ItemType.FILE, getFileName(uri) ?: "unknown", 0, TransferItem.TransferStatus.FAILED)
            } finally {
                showProgress(false)
            }
        }
    }
    
    private fun uploadImage(uri: Uri) {
        if (!checkConnection()) return
        
        scope.launch {
            try {
                showProgress(true)
                
                val fileName = getFileName(uri) ?: "image.jpg"
                val inputStream = contentResolver.openInputStream(uri)
                val bytes = inputStream?.readBytes()
                inputStream?.close()
                
                if (bytes == null) throw Exception("无法读取图片")
                
                val requestBody = bytes.toRequestBody("image/*".toMediaTypeOrNull())
                val multipartBody = MultipartBody.Part.createFormData(
                    "file",
                    fileName,
                    requestBody
                )
                
                val response = RetrofitClient.apiService.uploadFile(multipartBody)
                
                if (response.isSuccessful && response.body()?.success == true) {
                    addToHistory(ItemType.IMAGE, fileName, bytes.size.toLong())
                    showToast("✅ 图片上传成功！")
                } else {
                    throw Exception(response.body()?.message ?: "上传失败")
                }
            } catch (e: Exception) {
                showToast("❌ 上传失败: ${e.message}")
                addToHistory(ItemType.IMAGE, getFileName(uri) ?: "image.jpg", 0, TransferItem.TransferStatus.FAILED)
            } finally {
                showProgress(false)
            }
        }
    }
    
    private fun sendText(text: String) {
        if (!checkConnection()) return
        if (text.isEmpty()) {
            showToast("请输入文本内容")
            return
        }
        
        scope.launch {
            try {
                showProgress(true)
                
                val isLink = text.startsWith("http://") || text.startsWith("https://") || text.startsWith("www.")
                val type = if (isLink) ItemType.LINK else ItemType.TEXT
                
                val response = RetrofitClient.apiService.uploadText(TextRequest(text))
                
                if (response.isSuccessful && response.body()?.success == true) {
                    addToHistory(type, if (text.length > 30) text.substring(0, 30) + "..." else text, 0)
                    showToast("✅ 文本发送成功！")
                } else {
                    throw Exception(response.body()?.message ?: "发送失败")
                }
            } catch (e: Exception) {
                showToast("❌ 发送失败: ${e.message}")
            } finally {
                showProgress(false)
            }
        }
    }
    
    private fun showTextInputDialog() {
        if (!checkConnection()) return
        
        val editText = android.widget.EditText(this)
        editText.hint = "输入要发送的文本或链接..."
        editText.setPadding(50, 40, 50, 40)
        editText.textSize = 16f
        
        AlertDialog.Builder(this)
            .setTitle("📝 发送文本")
            .setView(editText)
            .setPositiveButton("发送") { _, _ ->
                val text = editText.text.toString().trim()
                if (text.isNotEmpty()) {
                    sendText(text)
                }
            }
            .setNegativeButton("取消", null)
            .show()
    }
    
    private fun pasteFromClipboard() {
        if (!checkConnection()) return
        
        val clipboard = getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager
        if (clipboard.hasPrimaryClip()) {
            val clipData = clipboard.primaryClip
            if (clipData != null && clipData.itemCount > 0) {
                val text = clipData.getItemAt(0).text.toString()
                if (text.isNotEmpty()) {
                    sendText(text)
                } else {
                    showToast("剪贴板为空")
                }
            }
        } else {
            showToast("剪贴板为空")
        }
    }
    
    private fun handleShareIntent(intent: Intent?) {
        if (intent?.action == Intent.ACTION_SEND) {
            val type = intent.type
            
            when {
                type?.startsWith("image/") == true -> {
                    val uri = intent.getParcelableExtra<Uri>(Intent.EXTRA_STREAM)
                    uri?.let { uploadImage(it) }
                }
                type == "text/plain" -> {
                    val text = intent.getStringExtra(Intent.EXTRA_TEXT)
                    text?.let {
                        AlertDialog.Builder(this)
                            .setTitle("📝 发送分享的文本")
                            .setMessage(it)
                            .setPositiveButton("发送") { _, _ ->
                                sendText(it)
                            }
                            .setNegativeButton("取消", null)
                            .show()
                    }
                }
                else -> {
                    val uri = intent.getParcelableExtra<Uri>(Intent.EXTRA_STREAM)
                    uri?.let { uploadFile(it) }
                }
            }
        }
    }
    
    private fun addToHistory(
        type: ItemType,
        fileName: String,
        fileSize: Long,
        status: TransferItem.TransferStatus = TransferItem.TransferStatus.SUCCESS
    ) {
        val item = TransferItem(
            type = type,
            fileName = fileName,
            fileSize = fileSize,
            status = status
        )
        historyList.add(0, item)
        historyAdapter.notifyItemInserted(0)
    }
    
    private fun showProgress(show: Boolean) {
        binding.cardProgress.visibility = if (show) View.VISIBLE else View.GONE
        if (show) {
            binding.progressBar.progress = 0
            binding.tvProgressText.text = "上传中..."
        }
    }
    
    private fun checkConnection(): Boolean {
        if (!isConnected) {
            showToast("⚠️ 请先连接服务器")
            return false
        }
        return true
    }
    
    private fun checkPermissions() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
            // Android 13+ 不需要存储权限
        } else if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.R) {
            // Android 11-12
            if (!hasPermission(Manifest.permission.READ_EXTERNAL_STORAGE)) {
                requestPermission(Manifest.permission.READ_EXTERNAL_STORAGE)
            }
        } else {
            // Android 10及以下
            if (!hasPermission(Manifest.permission.READ_EXTERNAL_STORAGE) ||
                !hasPermission(Manifest.permission.WRITE_EXTERNAL_STORAGE)) {
                requestPermissions(
                    arrayOf(
                        Manifest.permission.READ_EXTERNAL_STORAGE,
                        Manifest.permission.WRITE_EXTERNAL_STORAGE
                    ),
                    100
                )
            }
        }
    }
    
    private fun hasPermission(permission: String): Boolean {
        return ContextCompat.checkSelfPermission(this, permission) == PackageManager.PERMISSION_GRANTED
    }
    
    private fun requestPermission(permission: String) {
        requestPermissions(arrayOf(permission), 100)
    }
    
    private fun getFileName(uri: Uri): String? {
        var result: String? = null
        if (uri.scheme == "content") {
            val cursor = contentResolver.query(uri, null, null, null, null)
            cursor?.use {
                if (it.moveToFirst()) {
                    val index = it.getColumnIndex(android.provider.OpenableColumns.DISPLAY_NAME)
                    if (index != -1) {
                        result = it.getString(index)
                    }
                }
            }
        }
        if (result == null) {
            result = uri.path
            val cut = result?.lastIndexOf('/')
            if (cut != null && cut != -1) {
                result = result?.substring(cut + 1)
            }
        }
        return result
    }
    
    private fun showToast(message: String) {
        Toast.makeText(this, message, Toast.LENGTH_SHORT).show()
    }
    
    override fun onDestroy() {
        super.onDestroy()
        scope.cancel()
    }
}
