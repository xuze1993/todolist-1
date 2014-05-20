package com.gaotianpu.ftodo;

import com.loopj.android.http.*;

public class FTDClient {
	private static final String BASE_URL = "http://ftodo.sinaapp.com/";

	private static AsyncHttpClient client = new AsyncHttpClient();

	public static void post_new_task(long cust_id, String content,
			String device_type, String devie_no, long local_id,
			int creation_date, AsyncHttpResponseHandler responseHandler) {

		String url = BASE_URL + "new";

		RequestParams params = new RequestParams();
		params.put("cust_id", cust_id);
		params.put("body", content);
		params.put("creation_date", creation_date); // ���ĸ�Ϊ׼�أ�
		params.put("device_type", device_type);
		params.put("device_no", devie_no);
		params.put("local_id", local_id);

		client.post(url, params, responseHandler);
		return;

		// local_uniq_id = {cust_id}_{device_no}_{sqlite_pk_id}
		// remote_id = Զ�̵�pk_id

		// ���������� local_uniq_id,body,creation_date,cust_id
		// Ȩ����֤������
	}

	public static void load_by_custId(int cust_id, int page_index,
			int page_size,String order, AsyncHttpResponseHandler responseHandler) {
		String url = BASE_URL + "list";

		RequestParams params = new RequestParams();
		params.put("cust_id", cust_id);
		params.put("page_index", page_index);
		params.put("page_size", page_size);
		client.get(url, params, responseHandler);
		return;

	}

}