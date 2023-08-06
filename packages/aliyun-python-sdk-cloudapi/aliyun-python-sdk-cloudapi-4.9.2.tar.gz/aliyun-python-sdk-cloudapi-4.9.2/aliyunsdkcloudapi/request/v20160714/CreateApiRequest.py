# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from aliyunsdkcore.request import RpcRequest
from aliyunsdkcloudapi.endpoint import endpoint_data

class CreateApiRequest(RpcRequest):

	def __init__(self):
		RpcRequest.__init__(self, 'CloudAPI', '2016-07-14', 'CreateApi','apigateway')
		if hasattr(self, "endpoint_map"):
			setattr(self, "endpoint_map", endpoint_data.getEndpointMap())
		if hasattr(self, "endpoint_regional"):
			setattr(self, "endpoint_regional", endpoint_data.getEndpointRegional())


	def get_WebSocketApiType(self):
		return self.get_query_params().get('WebSocketApiType')

	def set_WebSocketApiType(self,WebSocketApiType):
		self.add_query_param('WebSocketApiType',WebSocketApiType)

	def get_ErrorCodeSamples(self):
		return self.get_query_params().get('ErrorCodeSamples')

	def set_ErrorCodeSamples(self,ErrorCodeSamples):
		self.add_query_param('ErrorCodeSamples',ErrorCodeSamples)

	def get_AppCodeAuthType(self):
		return self.get_query_params().get('AppCodeAuthType')

	def set_AppCodeAuthType(self,AppCodeAuthType):
		self.add_query_param('AppCodeAuthType',AppCodeAuthType)

	def get_Description(self):
		return self.get_query_params().get('Description')

	def set_Description(self,Description):
		self.add_query_param('Description',Description)

	def get_DisableInternet(self):
		return self.get_query_params().get('DisableInternet')

	def set_DisableInternet(self,DisableInternet):
		self.add_query_param('DisableInternet',DisableInternet)

	def get_ConstantParameters(self):
		return self.get_query_params().get('ConstantParameters')

	def set_ConstantParameters(self,ConstantParameters):
		self.add_query_param('ConstantParameters',ConstantParameters)

	def get_AuthType(self):
		return self.get_query_params().get('AuthType')

	def set_AuthType(self,AuthType):
		self.add_query_param('AuthType',AuthType)

	def get_AllowSignatureMethod(self):
		return self.get_query_params().get('AllowSignatureMethod')

	def set_AllowSignatureMethod(self,AllowSignatureMethod):
		self.add_query_param('AllowSignatureMethod',AllowSignatureMethod)

	def get_ServiceParameters(self):
		return self.get_query_params().get('ServiceParameters')

	def set_ServiceParameters(self,ServiceParameters):
		self.add_query_param('ServiceParameters',ServiceParameters)

	def get_FailResultSample(self):
		return self.get_query_params().get('FailResultSample')

	def set_FailResultSample(self,FailResultSample):
		self.add_query_param('FailResultSample',FailResultSample)

	def get_SystemParameters(self):
		return self.get_query_params().get('SystemParameters')

	def set_SystemParameters(self,SystemParameters):
		self.add_query_param('SystemParameters',SystemParameters)

	def get_ServiceParametersMap(self):
		return self.get_query_params().get('ServiceParametersMap')

	def set_ServiceParametersMap(self,ServiceParametersMap):
		self.add_query_param('ServiceParametersMap',ServiceParametersMap)

	def get_SecurityToken(self):
		return self.get_query_params().get('SecurityToken')

	def set_SecurityToken(self,SecurityToken):
		self.add_query_param('SecurityToken',SecurityToken)

	def get_OpenIdConnectConfig(self):
		return self.get_query_params().get('OpenIdConnectConfig')

	def set_OpenIdConnectConfig(self,OpenIdConnectConfig):
		self.add_query_param('OpenIdConnectConfig',OpenIdConnectConfig)

	def get_RequestParameters(self):
		return self.get_query_params().get('RequestParameters')

	def set_RequestParameters(self,RequestParameters):
		self.add_query_param('RequestParameters',RequestParameters)

	def get_ResultDescriptions(self):
		return self.get_query_params().get('ResultDescriptions')

	def set_ResultDescriptions(self,ResultDescriptions):
		self.add_query_param('ResultDescriptions',ResultDescriptions)

	def get_Visibility(self):
		return self.get_query_params().get('Visibility')

	def set_Visibility(self,Visibility):
		self.add_query_param('Visibility',Visibility)

	def get_GroupId(self):
		return self.get_query_params().get('GroupId')

	def set_GroupId(self,GroupId):
		self.add_query_param('GroupId',GroupId)

	def get_ServiceConfig(self):
		return self.get_query_params().get('ServiceConfig')

	def set_ServiceConfig(self,ServiceConfig):
		self.add_query_param('ServiceConfig',ServiceConfig)

	def get_ResultType(self):
		return self.get_query_params().get('ResultType')

	def set_ResultType(self,ResultType):
		self.add_query_param('ResultType',ResultType)

	def get_ApiName(self):
		return self.get_query_params().get('ApiName')

	def set_ApiName(self,ApiName):
		self.add_query_param('ApiName',ApiName)

	def get_ResultSample(self):
		return self.get_query_params().get('ResultSample')

	def set_ResultSample(self,ResultSample):
		self.add_query_param('ResultSample',ResultSample)

	def get_ForceNonceCheck(self):
		return self.get_query_params().get('ForceNonceCheck')

	def set_ForceNonceCheck(self,ForceNonceCheck):
		self.add_query_param('ForceNonceCheck',ForceNonceCheck)

	def get_RequestConfig(self):
		return self.get_query_params().get('RequestConfig')

	def set_RequestConfig(self,RequestConfig):
		self.add_query_param('RequestConfig',RequestConfig)

	def get_ResultBodyModel(self):
		return self.get_query_params().get('ResultBodyModel')

	def set_ResultBodyModel(self,ResultBodyModel):
		self.add_query_param('ResultBodyModel',ResultBodyModel)