package com.gaotianpu.ftodo.da;

public class SubjectBean {
	public static final String PK_ID = "pk_id";
	public static final String BODY = "body";
	public static final String CREATION_DATE = "creation_date";
	
	private long pk_id;
	private long remote_id;
	private long user_id;
	private String body;
	private String creation_date;
	private String update_date;
	
	private int is_todo=0;
	private int is_remind=0; 
	
	
	public long getId() {
		return pk_id;
	}
	public void setId(long id) {
		this.pk_id = id;
	}
	
	public long getUserId() {
		return user_id;
	}
	public void setUserId(long user_id) {
		this.user_id = user_id;
	}
	
	public String getBody() {
		return body;
	}
	public void setBody(String body) {
		this.body = body;
	}
	public String getCreationDate() {
		return creation_date;
	}
	public void setCreationDate(String creation_date) {
		this.creation_date = creation_date;
	}
	
	public String getUpdateDate() {
		return update_date;
	}
	public void setUpdateDate(String update_date) {
		this.update_date = update_date;
	}
	
	public long getRemoteId() {
		return remote_id;
	}
	public void setRemoteId(long id) {
		this.remote_id = id;
	}
	
	//
	public int getIsTodo() {
		return is_todo;
	}
	public void setIsTodo(int t) {
		this.is_todo = t;
	}
	//
	public int getIsRemind() {
		return is_remind;
	}
	public void setIsRemind(int r) {
		this.is_remind = r;
	}
	//
}
