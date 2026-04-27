package com.transferapp.filetransfer.network

import okhttp3.MultipartBody
import okhttp3.RequestBody
import retrofit2.Response
import retrofit2.http.*

interface ApiService {
    
    @GET("api/devices")
    suspend fun getDeviceInfo(): Response<DeviceResponse>
    
    @Multipart
    @POST("api/upload/file")
    suspend fun uploadFile(
        @Part file: MultipartBody.Part
    ): Response<UploadResponse>
    
    @POST("api/upload/text")
    suspend fun uploadText(
        @Body request: TextRequest
    ): Response<UploadResponse>
    
    @GET("api/files")
    suspend fun listFiles(): Response<FileListResponse>
}

data class DeviceResponse(
    val success: Boolean,
    val ip: String,
    val port: Int,
    val url: String,
    val device_name: String,
    val status: String
)

data class UploadResponse(
    val success: Boolean,
    val message: String? = null,
    val filename: String? = null
)

data class TextRequest(
    val text: String
)

data class FileListResponse(
    val success: Boolean,
    val files: List<FileInfo>
)

data class FileInfo(
    val filename: String,
    val size: Long,
    val created: String
)
